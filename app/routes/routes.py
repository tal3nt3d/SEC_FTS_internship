"""First router."""

from fastapi import APIRouter
from app.routes.tasks import tasks_router
from app.routes.comments import comments_router
from app.routes.users import users_router

main_router = APIRouter()
main_router.include_router(router=tasks_router)
main_router.include_router(router=comments_router)
main_router.include_router(router=users_router)

@main_router.get("/")
async def root():
    return {"message": "Hello World"}

@main_router.get("/health")
async def health_check():
    return {"status": "ok"}
    