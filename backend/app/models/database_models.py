from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class query_history(Base):
    __tablename__ = "NLPtoSQL"
    id = Column(Integer, primary_key = True, autoincrement=True)  
    user_id= Column(Integer)          
    user_query= Column(String)           
    generated_sql= Column(String)     
    