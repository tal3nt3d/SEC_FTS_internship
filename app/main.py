"""Entry point."""

from fastapi import FastAPI
import uvicorn
from app.config.settings import settings
from app.config.logger import logger
from app.routes.routes import main_router
from app.exceptions.handler import validation_exception_handler, app_exception_handler
from app.exceptions.errors import AppException
from fastapi.exceptions import RequestValidationError
from app.database.database import Base, engine

def create_app() -> FastAPI:
    app = FastAPI(title="Task Tracker API")
    app.include_router(main_router)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(AppException, app_exception_handler)
    return app

Base.metadata.create_all(bind=engine)

app = create_app()

if __name__ == "__main__":
    logger.info(f"Starting app in {settings.APP_ENV} mode")
    logger.info(f"Starting with settings: %s", settings.safe_settings)
    uvicorn.run("main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=settings.DEBUG)    
