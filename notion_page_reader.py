import sqlite3
from datetime import datetime
import json
import os
import argparse

class NotionPageReader:
    @staticmethod
    def _convert_to_markdown(block, debug=False):
        """將Notion塊轉換為Markdown格式

        Args:
            block (dict): Notion塊數據

        Returns:
            str: Markdown格式的文本
        """
        block_type = block['type']
        md = []
        has_content = False
        
        # 添加層級標記
        level_prefix = "#" * block['level'] if block['level'] else ""
        
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
                    md.append(f"# {text}")
                elif block_type in ['heading2', 'sub_header']:
                    md.append(f"## {text}")
                elif block_type in ['heading3', 'sub_sub_header']:
                    md.append(f"### {text}")
                elif block_type == 'bulleted_list_item':
                    md.append(f"- {text}")
                elif block_type == 'numbered_list_item':
                    md.append(f"1. {text}")
                elif block_type == 'to_do':
                    md.append(f"- [ ] {text}")
                elif block_type == 'toggle':
                    md.append(f"> {text}")
                elif block_type == 'quote':
                    md.append(f"> {text}")
                elif block_type == 'callout':
                    md.append(f"💡 {text}")
                elif block_type == 'code':
                    md.append(f"```\n{text}\n```")
                else:  # paragraph 或其他文本類型
                    md.append(text)
                has_content = True

        elif block_type == 'divider':
            md.append("---")
            has_content = True
            
        elif block_type == 'table':
            if block['content']:
                md.append("\n表格：")
                for row_id in block['content']:
                    md.append(f"- {row_id}")
                has_content = True
                    
        elif block_type == 'table_row':
            if block['properties']:
                cells = []
                for key, value in block['properties'].items():
                    cell_text = parse_rich_text(value)
                    if cell_text:
                        cells.append(cell_text)
                if cells:
                    md.append("| " + " | ".join(cells) + " |")
                    has_content = True

        elif block_type == 'image' and block['properties'] and 'source' in block['properties']:
            source = block['properties']['source'][0][0]
            title = block['properties'].get('title', [['image']])[0][0]
            md.append(f"![{title}]({source})")
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
            
        # 在調試模式下，始終返回內容，否則只在有內容時返回
        return "\n".join(md) if (debug or has_content) else None
    def _build_block_tree(self, blocks):
        """構建塊的樹狀結構

        Args:
            blocks (list): 塊列表

        Returns:
            dict: 塊的樹狀結構
        """
        # 創建ID到塊的映射
        block_map = {block['id']: block for block in blocks}
        
        # 初始化每個塊的子塊列表
        for block in blocks:
            block['children'] = []

        # 構建樹狀結構
        root_blocks = []
        for block in blocks:
            parent_id = block['parent_id']
            if parent_id in block_map:
                block_map[parent_id]['children'].append(block)
            else:
                root_blocks.append(block)

        return root_blocks

    def _format_block_tree(self, blocks, level=0, parent_type=None):
        """遞歸格式化塊樹

        Args:
            blocks (list): 塊列表
            level (int): 當前縮進層級
            parent_type (str): 父塊類型

        Returns:
            list: 格式化後的文本行
        """
        lines = []
        for block in blocks:
            # 獲取當前塊的markdown
            markdown = self._convert_to_markdown(block)
            if markdown:
                # 根據父類型添加適當的縮進
                if parent_type in ['numbered_list', 'bulleted_list']:
                    markdown = "    " * (level - 1) + markdown
                lines.append(markdown)
            
            # 遞歸處理子塊
            if block['children']:
                child_lines = self._format_block_tree(
                    block['children'],
                    level + 1,
                    block['type']
                )
                lines.extend(child_lines)
                
        return lines

    def __init__(self, db_path):
        """初始化NotionPageReader

        Args:
            db_path (str): Notion數據庫文件的路徑
        """
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"找不到數據庫文件：{db_path}")
        
        self.db_path = db_path
        
    def connect(self):
        """連接到Notion數據庫"""
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            raise Exception(f"連接數據庫時發生錯誤：{str(e)}")

    def get_page_blocks(self, page_id):
        """獲取指定頁面的所有塊

        Args:
            page_id (str): 頁面ID

        Returns:
            list: 塊列表
        """
        try:
            conn = self.connect()
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
                ORDER BY level ASC, CASE
                    WHEN type = 'header' THEN 1
                    WHEN type = 'sub_header' THEN 2
                    WHEN type = 'sub_sub_header' THEN 3
                    ELSE 4
                END,
                last_edited_time ASC
            """
            
            cursor.execute(query, (page_id,))
            columns = [description[0] for description in cursor.description]
            blocks = []
            
            for row in cursor.fetchall():
                block = dict(zip(columns, row))
                
                # 轉換時間戳
                if block['created_time']:
                    block['created_time'] = datetime.fromtimestamp(block['created_time'] / 1000)
                if block['last_edited_time']:
                    block['last_edited_time'] = datetime.fromtimestamp(block['last_edited_time'] / 1000)
                
                # 解析properties JSON
                if block['properties']:
                    try:
                        block['properties'] = json.loads(block['properties'])
                    except json.JSONDecodeError:
                        block['properties'] = None
                
                # 解析content JSON（如果存在）
                if block['content']:
                    try:
                        block['content'] = json.loads(block['content'])
                    except json.JSONDecodeError:
                        block['content'] = None
                
                blocks.append(block)
            
            return blocks
            
        except sqlite3.Error as e:
            raise Exception(f"查詢數據庫時發生錯誤：{str(e)}")
        finally:
            conn.close()

def main():
    """主函數"""
    parser = argparse.ArgumentParser(description='讀取Notion頁面的所有塊')
    parser.add_argument('page_id', help='Notion頁面ID')
    parser.add_argument('--debug', action='store_true', help='啟用調試模式，顯示詳細信息')
    args = parser.parse_args()

    db_path = "/Users/ronnie/Library/Application Support/Notion/notion.db"
    
    try:
        reader = NotionPageReader(db_path)
        blocks = reader.get_page_blocks(args.page_id)
        
        print(f"# 頁面內容 - {args.page_id}\n")
        
        if args.debug:
            print(f"找到 {len(blocks)} 個塊\n")
        
        for block in blocks:
            markdown = NotionPageReader._convert_to_markdown(block, debug=args.debug)
            if markdown:  # 在調試模式下或有內容時輸出
                print(f"{markdown}\n")
                if args.debug:
                    print("---\n")  # 在調試模式下添加分隔符
            
    except Exception as e:
        print(f"錯誤：{str(e)}")

if __name__ == "__main__":
    main()