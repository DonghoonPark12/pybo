import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(__file__), "../.env"))

    database_url: str = ""

@lru_cache
def get_settings() -> Settings:
    return Settings()