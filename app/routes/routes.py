"""First router."""

from fastapi import APIRouter, FastAPI
from routes.tasks import tasks_router
from routes.comments import comments_router
from routes.users import users_router

main_router = APIRouter()

@main_router.get("/")
async def root():
    return {"message": "Hello World"}

@main_router.get("/health")
async def health_check():
    return {"status": "ok"}

def register_routers(app: FastAPI) -> None:
    """Register all application routers."""
    app.include_router(router=main_router)
    app.include_router(router=tasks_router)
    app.include_router(router=comments_router)
    app.include_router(router=users_router)