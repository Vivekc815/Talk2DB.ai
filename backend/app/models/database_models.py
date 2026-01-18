from sqlalchemy import Column, Integer, String, Float, Boolean, Text, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class query_history(Base):
    __tablename__ = "NLPtoSQL"
    id = Column(Integer, primary_key=True, autoincrement=True)  
    user_id = Column(Integer)          
    user_query = Column(String)           
    generated_sql = Column(String)

class database_schema(Base):
    """Store extracted schemas from uploaded files or connections"""
    __tablename__ = "database_schemas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    schema_name = Column(String(100))  # e.g., "My Database", "SQL File Schema"
    schema_type = Column(String(50))  # "sql_file", "csv", "pdf", "database_connection"
    schema_data = Column(Text)  # JSON string of schema
    file_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=func.now())

class database_connection(Base):
    """Store database connection information (encrypted in production)"""
    __tablename__ = "database_connections"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    connection_name = Column(String(100))
    db_type = Column(String(50))  # "postgresql", "mysql", "sqlite"
    connection_string = Column(Text)  # Encrypted in production - store hashed/encrypted
    schema_id = Column(Integer)  # Reference to database_schema
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=func.now())
