import sqlite3
from datetime import datetime
import json
import os
import argparse

class NotionPageReader:
    def _convert_to_markdown(self, block, blocks, debug=False, level=0):
        """將Notion塊轉換為Markdown格式

        Args:
            block (dict): Notion塊數據
            blocks (list): 所有塊的列表
            debug (bool): 是否啟用調試模式
            level (int): 當前塊的層級（從0開始）

        Returns:
            str: Markdown格式的文本
        """
        block_type = block['type']
        md = []
        has_content = False

        # 添加縮進
        indent = "  " * level

        def parse_rich_text(rich_text):
            if not rich_text or not isinstance(rich_text, list):
                return ""
            text = ""
            for part in rich_text:
                if isinstance(part, list):
                    if len(part) == 1:
                        text += str(part[0])
                    elif len(part) == 2:
                        format_text = str(part[0])
                        formats = part[1]
                        if isinstance(formats, list):
                            for fmt in formats:
                                if fmt == ['b']:
                                    format_text = f"**{format_text}**"
                                elif fmt[0] == 'a':
                                    format_text = f"[{format_text}]({fmt[1]})"
                        text += format_text
            return text

        # 根據塊類型轉換
        if block['properties'] and 'title' in block['properties']:
            text = parse_rich_text(block['properties']['title'])
            if text.strip():
                if block_type in ['heading1', 'header']:
                    md.append(f"{indent}# {text}")
                elif block_type in ['heading2', 'sub_header']:
                    md.append(f"{indent}## {text}")
                elif block_type in ['heading3', 'sub_sub_header']:
                    md.append(f"{indent}### {text}")
                elif block_type == 'bulleted_list_item':
                    md.append(f"{indent}- {text}")
                elif block_type == 'numbered_list_item':
                    md.append(f"{indent}1. {text}")
                elif block_type == 'to_do':
                    md.append(f"{indent}- [ ] {text}")
                elif block_type == 'toggle':
                    md.append(f"{indent}> {text}")
                elif block_type == 'quote':
                    md.append(f"{indent}> {text}")
                elif block_type == 'callout':
                    md.append(f"{indent}💡 {text}")
                elif block_type == 'code':
                    md.append(f"{indent}```\n{text}\n{indent}```")
                else:  # paragraph 或其他文本類型
                    md.append(f"{indent}{text}")
                has_content = True

        elif block_type == 'divider':
            md.append(f"{indent}---")
            has_content = True
            
        elif block_type == 'table':
            if block['content']:
                md.append(f"{indent}\n表格：")
                for row_id in block['content']:
                    md.append(f"{indent}- {row_id}")
                has_content = True
                    
        elif block_type == 'table_row':
            if block['properties']:
                cells = []
                for key, value in block['properties'].items():
                    cell_text = parse_rich_text(value)
                    if cell_text:
                        cells.append(cell_text)
                if cells:
                    md.append(f"{indent}| " + " | ".join(cells) + " |")
                    has_content = True

        elif block_type == 'image' and block['properties'] and 'source' in block['properties']:
            source = block['properties']['source'][0][0]
            title = block['properties'].get('title', [['image']])[0][0]
            md.append(f"{indent}![{title}]({source})")
            has_content = True

        # 在調試模式下添加元數據
        if debug:
            md.append("\n=== 元數據 ===")
            md.append(f"類型: {block_type}")
            md.append(f"ID: {block['id']}")
            md.append(f"創建時間: {block['created_time']}")
            md.append(f"最後編輯時間: {block['last_edited_time']}")
            md.append(f"創建者: {block['created_by_name']}")
            md.append(f"父塊ID: {block['parent_id']}")
            if block['properties']:
                md.append("屬性:")
                md.append(json.dumps(block['properties'], ensure_ascii=False, indent=2))
            if block['content']:
                md.append("內容:")
                md.append(json.dumps(block['content'], ensure_ascii=False, indent=2))

        # 遞迴處理子塊
        if block['content']:
            for child_id in block['content']:
                child_block = next((b for b in blocks if b['id'] == child_id), None)
                if child_block:
                    child_md = self._convert_to_markdown(child_block, blocks, debug, level + 1)
                    if child_md:
                        md.append(child_md)

        # 在調試模式下，始終返回內容，否則只在有內容時返回
        return "\n".join(md) if (debug or has_content) else None
    
    def __init__(self, db_path):
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"找不到數據庫文件：{db_path}")
        self.db_path = db_path

    def connect(self):
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            raise Exception(f"連接Notion數據庫時發生錯誤：{e}")
            
    def get_page_blocks(self, page_id):
        """
        獲取指定頁面ID的所有塊。

        Args:
            page_id (str): 要獲取的頁面ID。

        Returns:
            list: 包含頁面所有塊的列表。
        """
        try:
            conn = self.connect()  # 確保這裡調用了self.connect()
            cursor = conn.cursor()
            query = """
                WITH RECURSIVE block_hierarchy AS (
                    -- 基礎查詢：獲取直接子塊
                    SELECT
                        block.id,
                        block.parent_id,
                        block.type,
                        block.properties,
                        block.content,
                        created_time,
                        created_by_id,
                        name AS created_by_name,
                        last_edited_time,
                        last_edited_by_id,
                        1 as level
                    FROM block
                    INNER JOIN notion_user ON notion_user.id = block.created_by_id
                    WHERE block.parent_id = ?

                    UNION ALL

                    -- 遞歸部分：獲取子塊的子塊
                    SELECT
                        b.id,
                        b.parent_id,
                        b.type,
                        b.properties,
                        b.content,
                        b.created_time,
                        b.created_by_id,
                        u.name,
                        b.last_edited_time,
                        b.last_edited_by_id,
                        h.level + 1
                    FROM block b
                    INNER JOIN block_hierarchy h ON h.id = b.parent_id
                    INNER JOIN notion_user u ON u.id = b.created_by_id
                )
                SELECT *
                FROM block_hierarchy
                """

            cursor.execute(query, (page_id,))
            columns = [description[0] for description in cursor.description]
            blocks = []

            for row in cursor.fetchall():
                block = dict(zip(columns, row))

                # 轉換時間戳記（如果存在）
                if block['created_time']:
                    block['created_time'] = datetime.fromtimestamp(block['created_time'] / 1000)
                if block['last_edited_time']:
                    block['last_edited_time'] = datetime.fromtimestamp(block['last_edited_time'] / 1000)

                # 解析 properties（如果存在）
                if block['properties']:
                    try:
                        block['properties'] = json.loads(block['properties'])
                    except json.JSONDecodeError:
                        block['properties'] = None

                # 解析 content（如果存在）
                if block['content']:
                    try:
                        block['content'] = json.loads(block['content'])
                    except json.JSONDecodeError:
                        block['content'] = None

                blocks.append(block)
            
            # 在此直接 return blocks
            return blocks

        except sqlite3.Error as e:
            print(f"Error querying database: {e}")
        finally:
            if conn:
                conn.close()

def main():
    parser = argparse.ArgumentParser(description='讀取Notion頁面的所有塊')
    parser.add_argument('page_id', help='Notion頁面ID')
    parser.add_argument('--debug', action='store_true', help='啟用調試模式，顯示詳細信息')
    args = parser.parse_args()

    db_path = os.path.expanduser("~/Library/Application Support/Notion/notion.db")
    reader = NotionPageReader(db_path)
    blocks = reader.get_page_blocks(args.page_id)
    
    print(f"# 頁面內容 - {args.page_id}\n")

    for block in blocks:
        # 僅在非debug模式下，過濾掉 level > 1 的 blocks
        if not args.debug and block['level'] > 1:
            continue
        
        markdown = reader._convert_to_markdown(block, blocks, debug=args.debug)
        if markdown:
            print(markdown)

if __name__ == "__main__":
    main()