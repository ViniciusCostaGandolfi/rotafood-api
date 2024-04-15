from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

database_conection = os.getenv("DATABASE_CONECTION_URL")

engine = create_engine(database_conection)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()
Base = declarative_base(metadata=metadata)