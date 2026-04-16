from storage.tasks import tasks_db
from exceptions.errors import TaskNotFoundError
from schemas.tasks import TaskCreate, TaskResponse, TaskUpdate

async def service_get_tasks():
    tasks = tasks_db
    if not tasks:
        raise TaskNotFoundError()
    return tasks

async def service_create_task(user_id: int, task_data: TaskCreate):
    task_db = {
        "id": len(tasks_db) + 1,
        "title": task_data.title,
        "description": task_data.description,
        "status": "pending",
        "user_id": user_id,
        "created_at": "2025-04-15T10:30:00Z",
        "updated_at": "2025-04-15T10:30:00Z"
    }
    tasks_db.append(task_db)
    return TaskResponse(**task_db)

async def service_get_task(task_id: int):
    for t in tasks_db:
        if t["id"] == task_id:
            task = TaskResponse(**t)
    if not task:
        raise TaskNotFoundError()
    return task

async def service_update_task(task_id: int, task_data: TaskUpdate):
    for t in tasks_db:
        if t["id"] == task_id:
            task_db = t
    task_db["title"] = task_data.title
    task_db["description"] = task_data.description
    task_db["status"] = task_data.status
    task_db["updated_at"] = "2025-04-15T10:30:00Z"
    return TaskResponse(**task_db)