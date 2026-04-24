"""Application settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path

CONFIG_DIR = Path(__file__).parent

def get_env_filename():
    env = os.getenv("APP_ENV", "dev")
    return f".env.{env}"

class Settings(BaseSettings):
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "my_database"    

    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DEBUG: bool = False
    LOG_LEVEL: str = "DEBUG"
    APP_ENV: str = "dev"
    
    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    model_config = SettingsConfigDict(env_file=str(CONFIG_DIR / get_env_filename()), extra='ignore')
    
    @property
    def safe_settings(self):
        return {
            "APP_HOST": self.APP_HOST,
            "APP_PORT": self.APP_PORT,
            "DEBUG": self.DEBUG,
            "LOG_LEVEL": self.LOG_LEVEL,
            "APP_ENV": self.APP_ENV,
            "DATABASE_URL": self.DATABASE_URL
        }

settings = Settings()
