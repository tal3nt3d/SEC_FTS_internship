"""Tasks router."""

from fastapi import APIRouter
from service.tasks import get_tasks

tasks_router = APIRouter(prefix="/tasks", tags=["tasks"])

@tasks_router.get("")
async def return_tasks():
    tasks = await get_tasks()
    return tasks
