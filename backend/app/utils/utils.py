from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def NLP_converted_SQL(query: str, schema: str = None):
    """Convert NLP to SQL with optional dynamic schema"""
    
    # Use provided schema or default
    if schema:
        schema_text = schema
    else:
        # Default schema (existing database)
        schema_text = """- students (id SERIAL [PK], name VARCHAR(100), age INTEGER, email VARCHAR(100), gpa DECIMAL(3,2), major VARCHAR(100), enrollment_year INTEGER, created_at TIMESTAMP)
- courses (id SERIAL [PK], name VARCHAR(100), code VARCHAR(20), credits INTEGER, department VARCHAR(100), created_at TIMESTAMP)
- teachers (id SERIAL [PK], name VARCHAR(100), department VARCHAR(100), email VARCHAR(100), years_experience INTEGER, created_at TIMESTAMP)"""
    
    messages = [{
        "role": "system", 
        "content": f"""You are a SQL query generator for PostgreSQL.

Database Schema:
{schema_text}
 
RULES:
1. Return ONLY the SQL query - NO explanations, NO markdown
2. Use proper PostgreSQL syntax
3. Return clean SQL without markdown formatting

Examples:
Input: "show all users"
Output: SELECT * FROM users;

Input: "find students with high GPA"
Output: SELECT * FROM students WHERE gpa > 3.5;"""
    }]
    
    messages.append({"role": "user", "content": f"{query}"})
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    # Clean up response (remove markdown if present)
    sql = response.choices[0].message.content.strip()
    if sql.startswith("```sql"):
        sql = sql.replace("```sql", "").replace("```", "").strip()
    elif sql.startswith("```"):
        sql = sql.replace("```", "").strip()
    
    return sql
