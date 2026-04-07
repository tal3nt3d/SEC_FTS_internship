"""Entry point."""

from fastapi import FastAPI
import uvicorn
from config.settings import settings
from config.logger import logger

app = FastAPI(title="Task Tracker API")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    print(f"Starting app in {settings.APP_ENV} mode")
    logger.info(f"Starting with settings: %s", settings.safe_settings)
    uvicorn.run("main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=settings.DEBUG)