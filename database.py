from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DB_URL = os.getenv("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DB_URL,connect_args={"check_same_thread":False})

SessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)
Base = declarative_base()

def init_db():
    if not os.path.exists(os.getenv("DATABASE_NAME")):
        Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db  # Return db session directly
    finally:
        db.close()

