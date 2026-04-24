"""Tasks router."""

from fastapi import APIRouter, Depends, status
from app.service.tasks import TaskService
from app.dependencies.tasks import get_task_service
from app.schemas.tasks import TaskResponse, TaskCreate, TaskUpdate, TaskFilter, TasksSummary
from fastapi.responses import StreamingResponse

tasks_router = APIRouter(prefix="/tasks", tags=["tasks"])

@tasks_router.get("", response_model=list[TaskResponse])
def get_tasks(filters: TaskFilter = Depends(), task_service: TaskService = Depends(get_task_service)):
    return task_service.get_tasks(filters)    
        
@tasks_router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(owner_id: int, task: TaskCreate, task_service: TaskService = Depends(get_task_service)):
    return task_service.create_task(owner_id, task)

@tasks_router.get("/summary", response_model=TasksSummary)
def get_summary(task_service: TaskService = Depends(get_task_service)):
    return task_service.get_summary()

@tasks_router.get("/export")
def export_tasks(task_service: TaskService = Depends(get_task_service)):
    csv_data = task_service.export_tasks()
    bom = '\ufeff'
    csv_data_with_bom = bom + csv_data
    encoded_data = csv_data_with_bom.encode('utf-8')
    return StreamingResponse(
        iter([encoded_data]),
        media_type="application/vnd.ms-excel",
        headers={"Content-Disposition": "attachment; filename=tasks_export.csv"}
    )
@tasks_router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, task_service: TaskService = Depends(get_task_service)):
    return task_service.get_task_by_id(task_id)

@tasks_router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, task_service: TaskService = Depends(get_task_service)):
    return task_service.update_task(task_id, task)

@tasks_router.post("/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: int, task_service: TaskService = Depends(get_task_service)):
    return task_service.complete_task(task_id)

@tasks_router.post("/{task_id}/assign", response_model=TaskResponse)
def assign_task(task_id: int, user_id: int, task_service: TaskService = Depends(get_task_service)):
    return task_service.assignee_task(task_id, user_id)

@tasks_router.post("/{task_id}/archive", response_model=TaskResponse)
def archive_task(task_id: int, task_service: TaskService = Depends(get_task_service)):
    return task_service.archive_task(task_id)
