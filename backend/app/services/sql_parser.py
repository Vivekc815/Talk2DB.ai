"""
SQL Parser Service
Extracts schema information from SQL files
"""
import re
from typing import Dict, List, Optional

def parse_sql_file(sql_content: str) -> Dict:
    """Parse SQL file to extract schema information"""
    schema = {
        "tables": [],
        "relationships": []
    }
    
    # Extract CREATE TABLE statements (case-insensitive, multiline)
    create_table_pattern = r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?["\']?(\w+)["\']?\s*\((.*?)\);'
    matches = re.finditer(create_table_pattern, sql_content, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    
    for match in matches:
        table_name = match.group(1)
        columns_str = match.group(2)
        columns = parse_columns(columns_str)
        
        schema["tables"].append({
            "name": table_name,
            "columns": columns
        })
    
    return schema

def parse_columns(columns_str: str) -> List[Dict]:
    """Parse column definitions from SQL CREATE TABLE statement"""
    columns = []
    
    # Split by comma, but be careful with nested parentheses
    column_parts = []
    current_part = ""
    paren_depth = 0
    
    for char in columns_str:
        if char == '(':
            paren_depth += 1
            current_part += char
        elif char == ')':
            paren_depth -= 1
            current_part += char
        elif char == ',' and paren_depth == 0:
            column_parts.append(current_part.strip())
            current_part = ""
        else:
            current_part += char
    
    if current_part.strip():
        column_parts.append(current_part.strip())
    
    for part in column_parts:
        if part.strip():
            column_info = parse_column_definition(part)
            if column_info:
                columns.append(column_info)
    
    return columns

def parse_column_definition(column_str: str) -> Optional[Dict]:
    """Parse a single column definition"""
    column_str = column_str.strip()
    
    # Skip constraints like PRIMARY KEY, FOREIGN KEY, etc. at table level
    if any(keyword in column_str.upper() for keyword in ['PRIMARY KEY', 'FOREIGN KEY', 'UNIQUE', 'CHECK', 'CONSTRAINT']):
        if 'FOREIGN KEY' in column_str.upper() or 'REFERENCES' in column_str.upper():
            # Extract relationship info if needed
            return None
        return None
    
    # Extract column name (first word)
    parts = column_str.split()
    if not parts:
        return None
    
    column_name = parts[0].strip('"\'')
    
    # Extract data type
    data_type = ""
    nullable = True
    is_primary = False
    
    if len(parts) > 1:
        # Get data type (second word, possibly with size)
        data_type = parts[1]
        if '(' in data_type:
            # Handle types like VARCHAR(100)
            end_paren = column_str.find(')', column_str.find('('))
            if end_paren > 0:
                data_type = column_str[column_str.find(parts[1][:parts[1].find('(')]):end_paren+1]
        else:
            data_type = parts[1]
    
    # Check for NOT NULL
    if 'NOT NULL' in column_str.upper():
        nullable = False
    
    # Check for PRIMARY KEY
    if 'PRIMARY KEY' in column_str.upper() or 'SERIAL PRIMARY KEY' in column_str.upper():
        is_primary = True
    
    return {
        "name": column_name,
        "type": data_type.upper(),
        "nullable": nullable,
        "primary_key": is_primary,
        "description": f"Column {column_name} of type {data_type}"
    }

def schema_to_text(schema: Dict) -> str:
    """Convert schema dictionary to text format for NLP"""
    schema_text = []
    
    for table in schema.get("tables", []):
        table_name = table["name"]
        columns = []
        
        for col in table.get("columns", []):
            col_str = f"{col['name']} ({col['type']})"
            if col.get('primary_key'):
                col_str += " [PK]"
            columns.append(col_str)
        
        schema_text.append(f"- {table_name} ({', '.join(columns)})")
    
    return "\n".join(schema_text)
