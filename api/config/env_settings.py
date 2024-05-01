from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    TOKEN_SECRET_KEY: str = ''
    
    ROTAFOOD_MS_LOGISTIC_URL: str = ''
    
    DATABASE_URL: str = ''
    
    EMAIL_PASSWORD: str = ''
    EMAIL_USERNAME: str = ''

    EMAIL_PORT: str = ''
    EMAIL_SERVER: str = ''

    IFOOD_GRANT_TYPE: str = ''
    IFOOD_CLIENT_ID: str = ''
    IFOOD_CLIENT_SECRET: str = ''

    model_config = SettingsConfigDict(env_file='.env', extra='allow')

    
settings = Settings()

print(settings)