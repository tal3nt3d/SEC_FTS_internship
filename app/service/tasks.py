from storage.tasks import tasks_db
from exceptions.errors import TaskNotFoundError
from schemas.tasks import TaskCreate, TaskResponse, TaskUpdate
from datetime import datetime

class TaskService:
    def __init__(self):
        self.tasks_db = tasks_db
    
    async def service_get_tasks(self):
        tasks = tasks_db
        if not tasks:
            raise TaskNotFoundError()
        return tasks

    async def service_create_task(self, user_id: int, task_data: TaskCreate):
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

    async def service_get_task(self, task_id: int):
        for t in tasks_db:
            if t["id"] == task_id:
                task = TaskResponse(**t)
        if not task:
            raise TaskNotFoundError()
        return task

    async def service_update_task(self, task_id: int, task_data: TaskUpdate):
        task_db = await self.service_get_task(task_id)
        task_db = task_db.model_dump()
        if task_data.title:
            task_db["title"] = task_data.title
        if task_data.description:
            task_db["description"] = task_data.description
        if task_data.status:
            task_db["status"] = task_data.status
        task_db["updated_at"] = datetime.now().isoformat()
        return TaskResponse(**task_db)