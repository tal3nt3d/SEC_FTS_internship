"""Application settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    APP_ENV: str = "dev"
    
    model_config = SettingsConfigDict(env_file=".env")
    
    @property
    def safe_settings(self):
        return {
            "APP_HOST": self.APP_HOST,
            "APP_PORT": self.APP_PORT,
            "DEBUG": self.DEBUG,
            "LOG_LEVEL": self.LOG_LEVEL,
            "APP_ENV": self.APP_ENV
        }

env = os.getenv("APP_ENV", "dev")

if env == "test":
    env_file = ".env.test"
elif env == "dev":
    env_file = ".env.dev"
else:
    env_file = ".env"
    
settings = Settings()
