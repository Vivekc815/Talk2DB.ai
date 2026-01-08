from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.utils import NLP_converted_SQL
from app.services.query_validator import sql_safety
import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from app.api.v1.history import history_store
from app.core.database import session, engine
from app.models import database_models
from app.models.database_models import query_history
from sqlalchemy import text

database_models.Base.metadata.create_all(bind = engine)
db = session()


load_dotenv()
class HistorySaveRequest(BaseModel):
    user_id: int
    user_query: str
    generated_sql: str


class QueryRequest(BaseModel):
    user_id : int
    query: str
def save_to_db(user_id, user_query, generated_sql):
        new_record = query_history(
            user_id=user_id,
            user_query=user_query,
            generated_sql=generated_sql
            )
        db.add(new_record)
        db.commit()

# Create FastAPI app
app = FastAPI(
    title="Talk2DB API",
    description="Natural language to SQL query system",
    version="1.0.0"
)

# CORS middleware (allows frontend to call API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
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
        "docs": "/docs"
    }




@app.post("/answer")
def sanitize_sql(request: QueryRequest):
    sql = request.query
    description = NLP_converted_SQL(sql)  # NLP generates SQL

    # Safety check
    TF_output, summary = sql_safety(description)

    # Execute only if safe
    results = None
    if TF_output:
        try:
            results = db.execute(text(description)).fetchall()
            # Convert rows to dict
            results = [dict(row._mapping) for row in results]
        except Exception as e:
            TF_output = False
            summary = str(e)

    # Save to DB history
    save_to_db(request.user_id, sql, description)

    # Return response
    return {
        "query": sql,
        "sql": description,
        "is_safe": TF_output,
        "error": summary if not TF_output else None,
        "results": results if TF_output else None
    }


    

@app.get("/history/{user_id}")
def get_history(user_id):
    records = db.query(query_history)\
                .filter(query_history.user_id == user_id)\
                .all()
    return {"data": records}



