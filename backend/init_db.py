#!/usr/bin/env python3
"""
Database initialization script for Render deployment.
Run this once after deploying to create tables and insert sample data.
"""
import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def init_database():
    # Get database URL
    db_url = os.getenv("DATABASE_URL")
    
    if not db_url:
        print("ERROR: DATABASE_URL not found in environment variables")
        sys.exit(1)
    
    # Handle Render's DATABASE_URL format
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    
    try:
        engine = create_engine(db_url)
        
        # Read SQL file
        sql_file_path = os.path.join(os.path.dirname(__file__), "app", "utils", "students.sql")
        
        if not os.path.exists(sql_file_path):
            print(f"ERROR: SQL file not found at {sql_file_path}")
            sys.exit(1)
        
        with open(sql_file_path, 'r') as f:
            sql_content = f.read()
        
        # Execute SQL
        with engine.connect() as conn:
            # Split by semicolon and execute each statement
            statements = [s.strip() for s in sql_content.split(';') if s.strip()]
            
            for statement in statements:
                if statement:
                    try:
                        conn.execute(text(statement))
                        conn.commit()
                    except Exception as e:
                        # Ignore errors for "IF NOT EXISTS" statements
                        if "already exists" not in str(e).lower():
                            print(f"Warning: {e}")
        
        print("✅ Database initialized successfully!")
        print("✅ Tables created and sample data inserted!")
        
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_database()
