import sqlite3
import os
import json
from textwrap import indent

class NotionSchemaReader:
    def __init__(self, db_path):
        """初始化NotionSchemaReader

        Args:
            db_path (str): Notion數據庫文件的路徑
        """
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"找不到數據庫文件：{db_path}")
        
        self.db_path = db_path
    
    def get_tables(self):
        """獲取所有表的信息
        
        Returns:
            list: 表信息列表
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 獲取所有表名
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' 
                ORDER BY name;
            """)
            tables = cursor.fetchall()
            
            results = []
            for (table_name,) in tables:
                # 獲取表結構
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                # 獲取索引信息
                cursor.execute(f"PRAGMA index_list({table_name})")
                indexes = cursor.fetchall()
                
                # 獲取外鍵信息
                cursor.execute(f"PRAGMA foreign_key_list({table_name})")
                foreign_keys = cursor.fetchall()
                
                # 獲取示例數據（最多3行）
                try:
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                    sample_data = cursor.fetchall()
                except sqlite3.Error:
                    sample_data = []
                
                results.append({
                    'name': table_name,
                    'columns': columns,
                    'indexes': indexes,
                    'foreign_keys': foreign_keys,
                    'sample_data': sample_data
                })
            
            return results
            
        except sqlite3.Error as e:
            raise Exception(f"查詢數據庫時發生錯誤：{str(e)}")
        finally:
            if conn:
                conn.close()
    
    def print_schema(self):
        """打印數據庫架構"""
        tables = self.get_tables()
        
        for table in tables:
            print(f"\n{'='*80}")
            print(f"表名: {table['name']}")
            print('='*80)
            
            print("\n列定義:")
            print("-"*40)
            for col in table['columns']:
                cid, name, type_, notnull, dflt_value, pk = col
                constraints = []
                if pk:
                    constraints.append("PRIMARY KEY")
                if notnull:
                    constraints.append("NOT NULL")
                if dflt_value is not None:
                    constraints.append(f"DEFAULT {dflt_value}")
                
                print(f"- {name:20} {type_:10} {' '.join(constraints)}")
            
            if table['indexes']:
                print("\n索引:")
                print("-"*40)
                for idx in table['indexes']:
                    print(f"- {idx[1]} ({idx[2]})")
            
            if table['foreign_keys']:
                print("\n外鍵:")
                print("-"*40)
                for fk in table['foreign_keys']:
                    print(f"- {fk[3]} -> {fk[2]}.{fk[4]}")
            
            if table['sample_data']:
                print("\n示例數據:")
                print("-"*40)
                for row in table['sample_data']:
                    formatted_row = []
                    for item in row:
                        if isinstance(item, str) and len(item) > 50:
                            formatted_row.append(f"{item[:47]}...")
                        else:
                            formatted_row.append(str(item))
                    print(f"| {' | '.join(formatted_row)} |")
            
            print()

def main():
    """主函數"""
    db_path = "/Users/ronnie/Library/Application Support/Notion/notion.db"
    
    try:
        reader = NotionSchemaReader(db_path)
        reader.print_schema()
    except Exception as e:
        print(f"錯誤：{str(e)}")

if __name__ == "__main__":
    main()
