# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # URL до PostgreSQL у форматі: postgresql+asyncpg://user:pass@host:port/dbname
    database_url: str
    env: str = "development"
    secret_key: str = "change-me"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

settings = Settings()