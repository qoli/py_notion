import sqlite3
from datetime import datetime
import json
import os
import argparse

class NotionPageReader:
    def _convert_to_markdown(self, block, blocks, debug=False, level=0):
        """Convert Notion blocks to Markdown format

        Args:
            block (dict): Notion block data
            blocks (list): List of all blocks
            debug (bool): Enable debug mode
            level (int): Current block level (starts from 0)

        Returns:
            str: Markdown formatted text
        """
        block_type = block['type']
        md = []
        has_content = False

        # Add indentation
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

        # Convert based on block type
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
                else:  # paragraph or other text types
                    md.append(f"{indent}{text}")
                has_content = True

        elif block_type == 'divider':
            md.append(f"{indent}---")
            has_content = True
            
        elif block_type == 'table':
            if block['content']:
                if debug:
                    md.append(f"{indent}\nTable:")
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

        # Add metadata in debug mode
        if debug:
            md.append("\n=== Metadata ===")
            md.append(f"Type: {block_type}")
            md.append(f"ID: {block['id']}")
            md.append(f"Created: {block['created_time']}")
            md.append(f"Last Edited: {block['last_edited_time']}")
            md.append(f"Creator: {block['created_by_name']}")
            md.append(f"Parent ID: {block['parent_id']}")
            md.append(f"Alive: {block['alive']}")
            if block['properties']:
                md.append("Properties:")
                md.append(json.dumps(block['properties'], ensure_ascii=False, indent=2))
            if block['content']:
                md.append("Content:")
                md.append(json.dumps(block['content'], ensure_ascii=False, indent=2))

        # Process child blocks if not page type
        if block['content'] and block_type != 'page':
            for child_id in block['content']:
                child_block = next((b for b in blocks if b['id'] == child_id), None)
                if child_block:
                    child_md = self._convert_to_markdown(child_block, blocks, debug, level + 1)
                    if child_md:
                        md.append(child_md)

        # Always return content in debug mode, otherwise only if has_content
        return "\n".join(md) if (debug or has_content) else None
    
    def __init__(self, db_path):
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found: {db_path}")
        self.db_path = db_path

    def connect(self):
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            raise Exception(f"Error connecting to Notion database: {e}")
            
    def get_page_blocks(self, page_id):
        """Get all blocks for the specified page ID. If page type, only return direct children.

        Args:
            page_id (str): The page ID to get blocks for.

        Returns:
            list: List containing all page blocks.
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            # Check page type
            cursor.execute("SELECT type FROM block WHERE id = ?", (page_id,))
            page_type = cursor.fetchone()
            
            if not page_type:
                return []
                
            if page_type[0] == 'page':
                # For page type, only get direct children
                query = """
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
                    1 as level,
                    block.alive
                FROM block
                INNER JOIN notion_user ON notion_user.id = block.created_by_id
                WHERE block.parent_id = ?
                """
            else:
                # For other types, use recursive query
                query = """
                WITH RECURSIVE block_hierarchy AS (
                    -- Base query: get direct children
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
                        1 as level,
                        block.alive
                    FROM block
                    INNER JOIN notion_user ON notion_user.id = block.created_by_id
                    WHERE block.parent_id = ?

                    UNION ALL

                    -- Recursive part: get children of children
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
                        h.level + 1,
                        b.alive
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

                # Convert timestamps if they exist
                if block['created_time']:
                    block['created_time'] = datetime.fromtimestamp(block['created_time'] / 1000)
                if block['last_edited_time']:
                    block['last_edited_time'] = datetime.fromtimestamp(block['last_edited_time'] / 1000)

                # Parse properties if they exist
                if block['properties']:
                    try:
                        block['properties'] = json.loads(block['properties'])
                    except json.JSONDecodeError:
                        block['properties'] = None

                # Parse content if it exists
                if block['content']:
                    try:
                        block['content'] = json.loads(block['content'])
                    except json.JSONDecodeError:
                        block['content'] = None

                blocks.append(block)
            
            return blocks

        except sqlite3.Error as e:
            print(f"Database query error: {e}")
        finally:
            if conn:
                conn.close()

def main():
    parser = argparse.ArgumentParser(description='Read all blocks from a Notion page')
    parser.add_argument('page_id', help='Notion page ID')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode to show detailed info')
    args = parser.parse_args()

    db_path = os.path.expanduser("~/Library/Application Support/Notion/notion.db")
    reader = NotionPageReader(db_path)
    blocks = reader.get_page_blocks(args.page_id)
    
    print(f"# Page Content - {args.page_id}\n")

    for block in blocks:
        # In non-debug mode, filter out blocks with level > 1 or alive != 1
        if not args.debug:
            if block['level'] > 1 or block['alive'] != 1:
                continue
        
        markdown = reader._convert_to_markdown(block, blocks, debug=args.debug)
        if markdown:
            print(markdown)

if __name__ == "__main__":
    main()