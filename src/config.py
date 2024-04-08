from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    
    DATABASE_URL: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    
    TOKEN_SECRET_KEY: str
    
    ROTAFOOD_MS_ROUTES_URL: str
    
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str
    EMAIL_SERVER: str
    EMAIL_PORT: str

    MINIO_FILE_PATH: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_URL: str
    MINIO_IMAGES_BUCKET_NAME: str
    
    IFOOD_GRANT_TYPE: str
    IFOOD_CLIENT_ID: str
    IFOOD_CLIENT_SECRET: str

    class Config:
        env_file = ".env"

settings = Settings()

