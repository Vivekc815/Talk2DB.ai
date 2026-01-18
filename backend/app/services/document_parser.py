"""
Document Parser Service
Extracts schema from PDF documents and CSV files
"""
import pandas as pd
import io
from typing import Dict, Optional

def parse_csv(file_content: bytes, filename: str = "uploaded_data") -> Dict:
    """Extract schema from CSV file"""
    try:
        # Read CSV
        df = pd.read_csv(io.BytesIO(file_content))
        
        # Infer column types
        columns = []
        for col in df.columns:
            dtype = str(df[col].dtype)
            
            # Map pandas dtypes to SQL types
            if 'int' in dtype:
                sql_type = 'INTEGER'
            elif 'float' in dtype:
                sql_type = 'DECIMAL'
            elif 'bool' in dtype:
                sql_type = 'BOOLEAN'
            elif 'datetime' in dtype:
                sql_type = 'TIMESTAMP'
            else:
                sql_type = 'VARCHAR(255)'
            
            columns.append({
                "name": col,
                "type": sql_type,
                "nullable": True,
                "primary_key": False,
                "description": f"Column from CSV file"
            })
        
        schema = {
            "tables": [{
                "name": filename.replace('.csv', '').replace('.CSV', ''),
                "columns": columns
            }]
        }
        
        return schema
    except Exception as e:
        raise Exception(f"Error parsing CSV: {str(e)}")

def parse_pdf_simple(file_content: bytes) -> Dict:
    """
    Simple PDF parser - extracts text and uses AI to identify schema
    For production, you might want to use pdfplumber or PyPDF2
    """
    # This is a placeholder - in production, you'd:
    # 1. Extract text from PDF using pdfplumber
    # 2. Use OpenAI to analyze text and extract schema
    # 3. Return structured schema
    
    return {
        "tables": [],
        "note": "PDF parsing requires text extraction and AI analysis"
    }

def extract_schema_with_ai(file_content: bytes, file_type: str, filename: str) -> Dict:
    """
    Use AI to extract schema from documents
    This would be called for PDF files or complex documents
    """
    from openai import OpenAI
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    if file_type == 'csv':
        return parse_csv(file_content, filename)
    
    # For PDF, extract text first (simplified - in production use pdfplumber)
    # Then use AI to understand structure
    # For now, return a placeholder
    return {
        "tables": [],
        "message": "PDF schema extraction requires text extraction. Use CSV or SQL files for now."
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
