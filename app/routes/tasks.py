"""Tasks router."""

from fastapi import APIRouter, Depends
from service.tasks import service_create_task, service_get_tasks, service_get_task, service_update_task
from schemas.tasks import TaskResponse, TaskCreate

tasks_router = APIRouter(prefix="/tasks", tags=["tasks"])

@tasks_router.get("", response_model=list[TaskResponse])
async def get_tasks():
    tasks = await service_get_tasks()
    return tasks
        
@tasks_router.post("/create", response_model=TaskResponse)
async def create_task(user_id: int, task: TaskCreate = Depends()):
    created_task = await service_create_task(user_id, task)
    return created_task

@tasks_router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int):
    task = await service_get_task(task_id)
    return task

@tasks_router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task: TaskCreate = Depends()):
    updated_task = await service_update_task(task_id, task)
    return updated_task