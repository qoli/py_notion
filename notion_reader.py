import sqlite3
from datetime import datetime
import json
import os

class NotionDatabaseReader:
    def __init__(self, db_path):
        """初始化NotionDatabaseReader

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

    def get_entries(self):
        """獲取Notion中的所有條目

        Returns:
            list: 條目列表
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            query = """
                WITH RECURSIVE page_hierarchy AS (
                    SELECT
                        id,
                        parent_id,
                        type,
                        properties,
                        1 as level,
                        id as root_page_id
                    FROM block
                    WHERE parent_table = 'space'
                    
                    UNION ALL
                    
                    SELECT
                        b.id,
                        b.parent_id,
                        b.type,
                        b.properties,
                        h.level + 1,
                        h.root_page_id
                    FROM block b
                    JOIN page_hierarchy h ON h.id = b.parent_id
                )
                SELECT DISTINCT
                    block.id,
                    space_id,
                    block.version,
                    block.type,
                    block.properties,
                    collection_id,
                    created_time,
                    created_by,
                    name AS "created_by_name",
                    last_edited_time,
                    last_edited_by,
                    block.parent_id,
                    ph.root_page_id,
                    ph.level
                FROM
                    block
                LEFT JOIN page_hierarchy ph ON block.id = ph.id
                INNER JOIN
                    notion_user
                ON
                    notion_user.id = block.created_by_id
                WHERE
                    last_edited_time IS NOT NULL
                ORDER BY
                    last_edited_time DESC
                LIMIT 20
            """
            
            cursor.execute(query)
            columns = [description[0] for description in cursor.description]
            entries = []
            
            for row in cursor.fetchall():
                entry = dict(zip(columns, row))
                
                # 轉換時間戳
                if entry['created_time']:
                    entry['created_time'] = datetime.fromtimestamp(entry['created_time'] / 1000)
                if entry['last_edited_time']:
                    entry['last_edited_time'] = datetime.fromtimestamp(entry['last_edited_time'] / 1000)
                
                # 解析properties JSON
                if entry['properties']:
                    try:
                        entry['properties'] = json.loads(entry['properties'])
                    except json.JSONDecodeError:
                        entry['properties'] = None
                
                entries.append(entry)
            
            return entries
            
        except sqlite3.Error as e:
            raise Exception(f"查詢數據庫時發生錯誤：{str(e)}")
        finally:
            conn.close()

def main():
    """主函數"""
    db_path = "/Users/ronnie/Library/Application Support/Notion/notion.db"
    try:
        reader = NotionDatabaseReader(db_path)
        entries = reader.get_entries()
        
        print(f"最新修改的 {len(entries)} 條記錄：")
        
        for i, entry in enumerate(entries, 1):
            print(f"\n--- 條目 {i} ---")
            print(f"ID: {entry['id']}")
            print(f"類型: {entry['type']}")
            print(f"創建時間: {entry['created_time']}")
            print(f"創建者: {entry['created_by_name']}")
            print(f"最後編輯時間: {entry['last_edited_time']}")
            print(f"所屬頁面ID: {entry['root_page_id'] if entry['root_page_id'] else '頂層空間'}")
            if entry['level']:
                print(f"頁面層級: {entry['level']}")
            if entry['properties']:
                print("屬性:")
                print(json.dumps(entry['properties'], ensure_ascii=False, indent=2))
            else:
                print("屬性: <空內容>")
            
    except Exception as e:
        print(f"錯誤：{str(e)}")

if __name__ == "__main__":
    main()