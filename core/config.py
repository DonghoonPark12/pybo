from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env")

    database_url: str = "mysql+pymysql://root:Chatbot1!@localhost:3306/pybo"

@lru_cache
def get_settings() -> Settings:
    return Settings()