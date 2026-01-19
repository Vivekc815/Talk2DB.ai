from fastapi import FastAPI, Depends, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from app.utils.utils import NLP_converted_SQL
from app.services.query_validator import sql_safety
from app.services.sql_parser import parse_sql_file, schema_to_text as sql_schema_to_text
from app.services.document_parser import parse_csv, parse_pdf, schema_to_text as doc_schema_to_text
from app.services.db_connector import get_schema_from_database, test_connection, create_db_engine, execute_query_on_db
import os
import json
import traceback
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
# from app.api.v1.history import history_store  # Not used, commented out
from app.core.database import SessionLocal, engine
from app.models import database_models
from app.models.database_models import query_history, database_schema
from sqlalchemy import text
from sqlalchemy.orm import Session

database_models.Base.metadata.create_all(bind=engine)

load_dotenv()

# Get environment variables
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", FRONTEND_URL).split(",") if os.getenv("ALLOWED_ORIGINS") else [FRONTEND_URL]

class HistorySaveRequest(BaseModel):
    user_id: int
    user_query: str
    generated_sql: str

class QueryRequest(BaseModel):
    user_id: int
    query: str
    schema_id: int = None  # Optional: use specific schema
    connection_id: int = None  # Optional: execute on connected database
    db_type: str = None  # Optional: for connected database
    connection_string: str = None  # Optional: for connected database

class SchemaRequest(BaseModel):
    user_id: int
    schema_name: str
    schema_type: str  # "sql_file", "csv", "database_connection"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_to_db(db: Session, user_id, user_query, generated_sql):
    try:
        new_record = query_history(
            user_id=user_id,
            user_query=user_query,
            generated_sql=generated_sql
        )
        db.add(new_record)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error saving to history: {e}")

# Create FastAPI app with increased request size limits
app = FastAPI(
    title="Talk2DB API",
    description="Natural language to SQL query system with file upload support",
    version="2.0.0"
)

# Increase request size limit for file uploads (default is 1MB, we need up to 10MB)
from fastapi import Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Note: Starlette (FastAPI's underlying framework) has a default max_request_size
# We'll handle this in the endpoint by checking file size

# CORS middleware - use environment variable in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint - test if server is running
@app.get("/")
def read_root():
    return {
        "message": "Welcome to Talk2DB API",
        "status": "running",
        "version": "2.0.0",
        "features": ["SQL file upload", "CSV file upload", "PDF file upload", "Database connections (PostgreSQL, MySQL)", "Dynamic schema support"],
        "docs": "/docs"
    }

@app.post("/answer")
def sanitize_sql(request: QueryRequest, db: Session = Depends(get_db)):
    sql = request.query
    schema_text = None
    
    # If schema_id provided, get schema from database
    if request.schema_id:
        try:
            schema_record = db.query(database_schema).filter(
                database_schema.id == request.schema_id,
                database_schema.user_id == request.user_id,
                database_schema.is_active == True
            ).first()
            
            if schema_record:
                schema_dict = json.loads(schema_record.schema_data)
                schema_text = doc_schema_to_text(schema_dict)
        except Exception as e:
            print(f"Error loading schema: {e}")
    
    # Generate SQL with schema
    description = NLP_converted_SQL(sql, schema_text)
    
    # Safety check
    TF_output, summary = sql_safety(description)
    
    # Execute only if safe (on default or connected database)
    results = None
    if TF_output:
        try:
            # If connection provided, execute on connected database
            if request.connection_string and request.db_type:
                query_result = execute_query_on_db(request.db_type, request.connection_string, description)
                if query_result["success"]:
                    results = query_result["results"]
                else:
                    TF_output = False
                    summary = query_result.get("error", "Query execution failed on connected database")
            else:
                # Execute on default database
                results = db.execute(text(description)).fetchall()
                # Convert rows to dict
                results = [dict(row._mapping) for row in results]
        except Exception as e:
            TF_output = False
            summary = str(e)
            db.rollback()
    
    # Save to DB history
    try:
        save_to_db(db, request.user_id, sql, description)
    except Exception as e:
        print(f"Error saving to history: {e}")
    
    # Return response
    return {
        "query": sql,
        "sql": description,
        "is_safe": TF_output,
        "error": summary if not TF_output else None,
        "results": results if TF_output else None,
        "schema_used": request.schema_id is not None
    }

@app.post("/upload/sql")
async def upload_sql_file(
    user_id: int = Form(...),
    schema_name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload SQL file and extract schema"""
    try:
        # Read file content
        content = await file.read()
        sql_content = content.decode('utf-8')
        
        # Parse SQL file
        schema_dict = parse_sql_file(sql_content)
        
        # Convert to text format
        schema_text = sql_schema_to_text(schema_dict)
        
        # Save schema to database
        schema_record = database_schema(
            user_id=user_id,
            schema_name=schema_name,
            schema_type="sql_file",
            schema_data=json.dumps(schema_dict),
            file_name=file.filename,
            is_active=True
        )
        db.add(schema_record)
        db.commit()
        db.refresh(schema_record)
        
        return {
            "success": True,
            "message": "SQL file uploaded and schema extracted successfully",
            "schema_id": schema_record.id,
            "schema": schema_dict,
            "schema_text": schema_text,
            "tables": schema_dict.get("tables", [])
        }
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/upload/csv")
async def upload_csv_file(
    user_id: int = Form(...),
    schema_name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload CSV file and extract schema"""
    try:
        # Read file content
        content = await file.read()
        filename = file.filename or "uploaded_data"
        
        # Parse CSV
        schema_dict = parse_csv(content, filename)
        
        # Convert to text format
        schema_text = doc_schema_to_text(schema_dict)
        
        # Save schema to database
        schema_record = database_schema(
            user_id=user_id,
            schema_name=schema_name,
            schema_type="csv",
            schema_data=json.dumps(schema_dict),
            file_name=file.filename,
            is_active=True
        )
        db.add(schema_record)
        db.commit()
        db.refresh(schema_record)
        
        return {
            "success": True,
            "message": "CSV file uploaded and schema extracted successfully",
            "schema_id": schema_record.id,
            "schema": schema_dict,
            "schema_text": schema_text,
            "tables": schema_dict.get("tables", [])
        }
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/upload/pdf")
async def upload_pdf_file(
    user_id: int = Form(...),
    schema_name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload PDF file and extract schema using AI"""
    try:
        print(f"PDF upload started: user_id={user_id}, schema_name={schema_name}, filename={file.filename}")
        
        # Validate file type
        if not file.filename or not file.filename.lower().endswith('.pdf'):
            return {
                "success": False,
                "error": "Invalid file type. Please upload a PDF file (.pdf extension required)."
            }
        
        # Read file content with timeout handling
        try:
            print(f"Reading PDF file content...")
            content = await file.read()
            filename = file.filename or "document"
            print(f"PDF file read successfully: {len(content)} bytes")
        except Exception as read_error:
            print(f"Error reading file: {str(read_error)}")
            traceback.print_exc()
            return {
                "success": False,
                "error": f"Network error: Failed to read uploaded file. Please check your internet connection and try again. Error: {str(read_error)}"
            }
        
        # Check file size (max 10MB)
        if len(content) > 10 * 1024 * 1024:
            return {
                "success": False,
                "error": "File too large. Please upload a PDF file smaller than 10MB."
            }
        
        if len(content) == 0:
            return {
                "success": False,
                "error": "PDF file is empty. Please upload a valid PDF file."
            }
        
        # Parse PDF with better error handling
        print(f"Starting PDF parsing...")
        try:
            schema_dict = parse_pdf(content, filename)
            print(f"PDF parsing completed")
        except Exception as parse_error:
            error_msg = str(parse_error)
            print(f"PDF parsing error: {error_msg}")
            traceback.print_exc()
            
            # Check for specific error types
            if "network" in error_msg.lower() or "timeout" in error_msg.lower() or "connection" in error_msg.lower():
                return {
                    "success": False,
                    "error": f"Network error during PDF processing: {error_msg}. Please check your internet connection and try again."
                }
            elif "openai" in error_msg.lower() or "api" in error_msg.lower():
                return {
                    "success": False,
                    "error": f"AI service error: {error_msg}. Please check your OpenAI API key configuration."
                }
            else:
                return {
                    "success": False,
                    "error": f"Error parsing PDF: {error_msg}. Make sure the PDF contains readable text (not scanned images)."
                }
        
        # Check if parsing returned an error
        if "error" in schema_dict:
            return {
                "success": False,
                "error": schema_dict["error"]
            }
        
        if not schema_dict.get("tables") or len(schema_dict.get("tables", [])) == 0:
            return {
                "success": False,
                "error": schema_dict.get("error", "No database schema found in PDF. Please ensure the PDF contains database documentation with table definitions (CREATE TABLE statements or table descriptions).")
            }
        
        # Convert to text format
        schema_text = doc_schema_to_text(schema_dict)
        
        # Save schema to database
        try:
            schema_record = database_schema(
                user_id=user_id,
                schema_name=schema_name,
                schema_type="pdf",
                schema_data=json.dumps(schema_dict),
                file_name=file.filename,
                is_active=True
            )
            db.add(schema_record)
            db.commit()
            db.refresh(schema_record)
        except Exception as db_error:
            db.rollback()
            print(f"Database error: {str(db_error)}")
            return {
                "success": False,
                "error": f"Error saving schema to database: {str(db_error)}"
            }
        
        return {
            "success": True,
            "message": "PDF file uploaded and schema extracted successfully",
            "schema_id": schema_record.id,
            "schema": schema_dict,
            "schema_text": schema_text,
            "tables": schema_dict.get("tables", [])
        }
    except Exception as e:
        db.rollback()
        print(f"PDF upload error: {str(e)}")
        traceback.print_exc()
        return {
            "success": False,
            "error": f"Failed to upload PDF: {str(e)}. Please check the file is a valid PDF and try again."
        }

@app.post("/connect/database")
def connect_database(
    user_id: int,
    schema_name: str,
    db_type: str,
    connection_string: str,
    db: Session = Depends(get_db)
):
    """Connect to external database and extract schema"""
    try:
        # Test connection
        if not test_connection(db_type, connection_string):
            return {
                "success": False,
                "error": "Failed to connect to database. Check connection string."
            }
        
        # Extract schema
        schema_dict = get_schema_from_database(db_type, connection_string)
        schema_text = doc_schema_to_text(schema_dict)
        
        # Save schema (don't save connection string for security - user will provide it each time)
        schema_record = database_schema(
            user_id=user_id,
            schema_name=schema_name,
            schema_type="database_connection",
            schema_data=json.dumps(schema_dict),
            file_name=None,
            is_active=True
        )
        db.add(schema_record)
        db.commit()
        db.refresh(schema_record)
        
        return {
            "success": True,
            "message": "Database connected and schema extracted successfully",
            "schema_id": schema_record.id,
            "schema": schema_dict,
            "schema_text": schema_text,
            "tables": schema_dict.get("tables", [])
        }
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/schemas/{user_id}")
def get_user_schemas(user_id: int, db: Session = Depends(get_db)):
    """Get all schemas for a user"""
    try:
        schemas = db.query(database_schema).filter(
            database_schema.user_id == user_id,
            database_schema.is_active == True
        ).all()
        
        result = []
        for schema in schemas:
            result.append({
                "id": schema.id,
                "schema_name": schema.schema_name,
                "schema_type": schema.schema_type,
                "file_name": schema.file_name,
                "created_at": str(schema.created_at),
                "tables": json.loads(schema.schema_data).get("tables", [])
            })
        
        return {"success": True, "schemas": result}
    except Exception as e:
        return {"success": False, "error": str(e), "schemas": []}

@app.get("/schemas/{user_id}/{schema_id}")
def get_schema_details(user_id: int, schema_id: int, db: Session = Depends(get_db)):
    """Get detailed schema information"""
    try:
        schema_record = db.query(database_schema).filter(
            database_schema.id == schema_id,
            database_schema.user_id == user_id,
            database_schema.is_active == True
        ).first()
        
        if not schema_record:
            return {"success": False, "error": "Schema not found"}
        
        schema_dict = json.loads(schema_record.schema_data)
        
        return {
            "success": True,
            "schema": schema_dict,
            "schema_text": doc_schema_to_text(schema_dict),
            "metadata": {
                "id": schema_record.id,
                "schema_name": schema_record.schema_name,
                "schema_type": schema_record.schema_type,
                "file_name": schema_record.file_name,
                "created_at": str(schema_record.created_at)
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.delete("/schemas/{user_id}/{schema_id}")
def delete_schema(user_id: int, schema_id: int, db: Session = Depends(get_db)):
    """Deactivate a schema"""
    try:
        schema_record = db.query(database_schema).filter(
            database_schema.id == schema_id,
            database_schema.user_id == user_id
        ).first()
        
        if not schema_record:
            return {"success": False, "error": "Schema not found"}
        
        schema_record.is_active = False
        db.commit()
        
        return {"success": True, "message": "Schema deactivated"}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}

@app.post("/query/database")
def query_connected_database(
    user_id: int,
    query: str,
    db_type: str,
    connection_string: str,
    db: Session = Depends(get_db)
):
    """
    Query a connected database using NLP
    This endpoint generates SQL from NLP and executes it on the connected database
    """
    try:
        # Extract schema from connected database
        schema_dict = get_schema_from_database(db_type, connection_string)
        schema_text = doc_schema_to_text(schema_dict)
        
        # Generate SQL with schema
        description = NLP_converted_SQL(query, schema_text)
        
        # Safety check
        TF_output, summary = sql_safety(description)
        
        # Execute on connected database
        results = None
        if TF_output:
            query_result = execute_query_on_db(db_type, connection_string, description)
            if query_result["success"]:
                results = query_result["results"]
            else:
                TF_output = False
                summary = query_result.get("error", "Query execution failed")
        
        # Save to history (on default DB, not connected DB)
        try:
            save_to_db(db, user_id, query, description)
        except Exception as e:
            print(f"Error saving to history: {e}")
        
        return {
            "query": query,
            "sql": description,
            "is_safe": TF_output,
            "error": summary if not TF_output else None,
            "results": results if TF_output else None,
            "schema_used": True,
            "database_type": db_type
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/history/{user_id}")
def get_history(user_id: int, db: Session = Depends(get_db)):
    try:
        records = db.query(query_history)\
                    .filter(query_history.user_id == user_id)\
                    .all()
        return {"data": records}
    except Exception as e:
        db.rollback()
        return {"error": str(e), "data": []}
