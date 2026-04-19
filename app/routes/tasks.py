"""Tasks router."""

from fastapi import APIRouter, Depends
from service.tasks import TaskService
from dependencies.tasks import get_task_service
from schemas.tasks import TaskResponse, TaskCreate, TaskUpdate, TaskFilter, TasksSummary
from fastapi.responses import StreamingResponse

tasks_router = APIRouter(prefix="/tasks", tags=["tasks"])

@tasks_router.get("", response_model=list[TaskResponse])
async def get_tasks(filters: TaskFilter = Depends(), task_service: TaskService = Depends(get_task_service)):
    return await task_service.service_get_tasks(filters)
        
@tasks_router.post("", response_model=TaskResponse)
async def create_task(user_id: int, task: TaskCreate, task_service: TaskService = Depends(get_task_service)):
    return await task_service.service_create_task(user_id, task)

@tasks_router.get("/summary", response_model=TasksSummary)
async def get_summary(task_service: TaskService = Depends(get_task_service)):
    return await task_service.service_get_summary()

@tasks_router.get("/export")
async def export_tasks(task_service: TaskService = Depends(get_task_service)):
    csv_data = await task_service.service_export_tasks()
    return StreamingResponse(
        iter([csv_data]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=tasks_export.csv"}
    )

@tasks_router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, task_service: TaskService = Depends(get_task_service)):
    return await task_service.service_get_task(task_id)

@tasks_router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task: TaskUpdate, task_service: TaskService = Depends(get_task_service)):
    return await task_service.service_update_task(task_id, task)

@tasks_router.post("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(task_id: int, task_service: TaskService = Depends(get_task_service)):
    return await task_service.service_complete_task(task_id)

@tasks_router.post("/{task_id}/assign", response_model=TaskResponse)
async def assign_task(task_id: int, user_id: int, task_service: TaskService = Depends(get_task_service)):
    return await task_service.service_assignee_task(task_id, user_id)

@tasks_router.post("/{task_id}/archive", response_model=TaskResponse)
async def archive_task(task_id: int, task_service: TaskService = Depends(get_task_service)):
    return await task_service.service_archive_task(task_id)
