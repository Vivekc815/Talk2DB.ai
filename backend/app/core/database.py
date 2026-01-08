from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
db_url = os.getenv("db_url")

engine = create_engine(db_url)
session = sessionmaker(autocommit = False, autoflush = False, bind = engine)