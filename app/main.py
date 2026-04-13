"""Entry point."""

from fastapi import FastAPI
import uvicorn
from config.settings import settings
from config.logger import logger
from routes.routes import main_router

app = FastAPI(title="Task Tracker API")

app.include_router(main_router)

if __name__ == "__main__":
    logger.info(f"Starting app in {settings.APP_ENV} mode")
    logger.info(f"Starting with settings: %s", settings.safe_settings)
    uvicorn.run("main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=settings.DEBUG)    
