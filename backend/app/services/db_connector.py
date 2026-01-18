"""
Database Connector Service
Handles connections to different database types
"""
from sqlalchemy import create_engine, inspect
from typing import Dict, Optional

def create_db_engine(db_type: str, connection_string: str):
    """Create database engine based on type"""
    if db_type.lower() == "postgresql":
        # Handle postgres:// to postgresql://
        if connection_string.startswith("postgres://"):
            connection_string = connection_string.replace("postgres://", "postgresql://", 1)
    elif db_type.lower() == "mysql":
        if not connection_string.startswith("mysql+pymysql://"):
            connection_string = connection_string.replace("mysql://", "mysql+pymysql://", 1)
    elif db_type.lower() == "sqlite":
        if not connection_string.startswith("sqlite:///"):
            connection_string = f"sqlite:///{connection_string}"
    
    return create_engine(connection_string)

def get_schema_from_database(db_type: str, connection_string: str) -> Dict:
    """Extract schema from live database connection"""
    try:
        engine = create_db_engine(db_type, connection_string)
        inspector = inspect(engine)
        
        schema = {"tables": []}
        
        # Get all table names
        table_names = inspector.get_table_names()
        
        for table_name in table_names:
            columns = []
            primary_keys = inspector.get_pk_constraint(table_name)['constrained_columns']
            
            # Get columns
            for column in inspector.get_columns(table_name):
                col_info = {
                    "name": column['name'],
                    "type": str(column['type']),
                    "nullable": column['nullable'],
                    "primary_key": column['name'] in primary_keys,
                    "description": f"Column from {table_name} table"
                }
                columns.append(col_info)
            
            schema["tables"].append({
                "name": table_name,
                "columns": columns
            })
        
        return schema
    except Exception as e:
        raise Exception(f"Error extracting schema from database: {str(e)}")

def test_connection(db_type: str, connection_string: str) -> bool:
    """Test if database connection works"""
    try:
        engine = create_db_engine(db_type, connection_string)
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception as e:
        return False
