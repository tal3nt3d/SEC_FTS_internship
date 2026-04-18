"""Tasks router."""

from fastapi import APIRouter, Depends
from service.tasks import TaskService
from dependencies.tasks import get_task_service
from schemas.tasks import TaskResponse, TaskCreate, TaskUpdate

tasks_router = APIRouter(prefix="/tasks", tags=["tasks"])

@tasks_router.get("", response_model=list[TaskResponse])
async def get_tasks(task_service: TaskService = Depends(get_task_service)):
    tasks = await task_service.service_get_tasks()
    return tasks
        
@tasks_router.post("", response_model=TaskResponse)
async def create_task(user_id: int, task: TaskCreate, task_service: TaskService = Depends(get_task_service)):
    created_task = await task_service.service_create_task(user_id, task)
    return created_task

@tasks_router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, task_service: TaskService = Depends(get_task_service)):
    task = await task_service.service_get_task(task_id)
    return task

@tasks_router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task: TaskUpdate, task_service: TaskService = Depends(get_task_service)):
    updated_task = await task_service.service_update_task(task_id, task)
    return updated_task