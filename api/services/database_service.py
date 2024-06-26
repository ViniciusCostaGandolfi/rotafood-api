from sqlalchemy.schema import MetaData
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.decl_api import declarative_base
from sqlalchemy.orm import sessionmaker
from api.config.env_settings import settings

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

database_conection = settings.DATABASE_URL
engine = create_engine(database_conection)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()
Base = declarative_base(metadata=metadata)