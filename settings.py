"""Application settings."""
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    APP_ENV: str = "dev"
    
    class Config:
        env_file = ".env"
    
    def get_safe_settings(self):
        return {
            "APP_HOST": self.APP_HOST,
            "APP_PORT": self.APP_PORT,
            "DEBUG": self.DEBUG,
            "LOG_LEVEL": self.LOG_LEVEL,
            "APP_ENV": self.APP_ENV
        }

env = os.getenv("APP_ENV", "dev")

if env == "test":
    settings = Settings(APP_HOST="127.0.0.1", APP_PORT=8001, DEBUG=False, LOG_LEVEL="INFO", APP_ENV="test")
elif env == "dev":
    settings = Settings(APP_HOST="127.0.0.1", APP_PORT=8000, DEBUG=True, LOG_LEVEL="DEBUG", APP_ENV="dev")
else:
    settings = Settings()
    