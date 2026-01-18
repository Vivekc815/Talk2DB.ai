"""
Document Parser Service
Extracts schema from PDF documents and CSV files
"""
import pandas as pd
import pdfplumber
import io
from typing import Dict, Optional
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

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

def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file"""
    try:
        pdf_file = io.BytesIO(file_content)
        text = ""
        
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def parse_pdf(file_content: bytes, filename: str = "document") -> Dict:
    """
    Parse PDF document using AI to extract schema information
    """
    try:
        # Extract text from PDF
        pdf_text = extract_text_from_pdf(file_content)
        
        if not pdf_text or len(pdf_text.strip()) < 50:
            return {
                "tables": [],
                "error": "PDF appears to be empty or could not extract text. Make sure the PDF contains readable text (not scanned images)."
            }
        
        # Use AI to extract schema from PDF text
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = f"""Analyze the following database documentation text and extract database schema information (tables and columns).

Text from PDF:
{pdf_text[:3000]}  # Limit to avoid token limits

Extract any CREATE TABLE statements, table definitions, or database schema information.
If you find database tables, list them in this format:

Table: table_name
- column1 (type) [description]
- column2 (type) [description]

Return the schema in JSON format:
{{
    "tables": [
        {{
            "name": "table_name",
            "columns": [
                {{"name": "column1", "type": "VARCHAR(100)", "nullable": true, "primary_key": false, "description": "description"}}
            ]
        }}
    ]
}}

If no schema is found, return empty tables array."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a database schema extraction expert. Extract table and column information from documentation."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        
        # Validate and format result
        if "tables" in result:
            return result
        else:
            return {"tables": []}
            
    except Exception as e:
        raise Exception(f"Error parsing PDF: {str(e)}")

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
