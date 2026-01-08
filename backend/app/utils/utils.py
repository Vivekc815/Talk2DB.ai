from openai import OpenAI
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def NLP_converted_SQL(query):
    messages = [{"role": "system", "content": """You are a SQL query generator for PostgreSQL.

Database Schema:
- students (id, name, age, email, gpa, major, enrollment_year, created_at)
- courses (id, name, code, credits, department, created_at)
- teachers (id, name, department, email, years_experience, created_at) 
 
RULES:
1. Return ONLY the SQL query - NO explanations, NO markdown


Examples:
Input: "show all users"
Output: SELECT * FROM users;"""}]
    messages.append({"role": "user", "content": f"{query}"})

    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages = messages
    )
    return(response.choices[0].message.content)



