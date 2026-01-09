from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment variable
# Render provides DATABASE_URL automatically when you add PostgreSQL
db_url = os.getenv("DATABASE_URL")

if not db_url:
    # Fallback for local development
    db_url = os.getenv("db_url", "postgresql://vivekchenganassery:Vivek%40123@localhost:5432/vivek")

# Handle Render's DATABASE_URL format (postgres:// -> postgresql://)
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal
