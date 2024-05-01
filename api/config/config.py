from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class ProductionSettings(BaseSettings):
    AUTH_SECRET_KEY: str
    ROTAFOOD_MS_LOGISTIC: str
    DATABASE_DNS: str
    model_config = SettingsConfigDict(env_prefix='')
    
class TestSettings(BaseSettings):
    AUTH_SECRET_KEY: str
    ROTAFOOD_MS_LOGISTIC: str
    DATABASE_DNS: str
    model_config = SettingsConfigDict(env_prefix='test')