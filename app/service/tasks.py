from storage.tasks import tasks_db
from exceptions.errors import TaskNotFoundError, TaskAlreadyCompletedError, TaskAlreadyArchivedError
from schemas.tasks import TaskCreate, TaskResponse, TaskUpdate, TaskFilter, TasksSummary
from datetime import datetime
import csv
from io import StringIO

class TaskService:
    def __init__(self):
        self.tasks_db = tasks_db
    
    async def service_get_tasks(self, filters: TaskFilter):
        tasks = self.tasks_db.copy()
        if filters.status: 
            tasks = [t for t in tasks if t["status"] == filters.status]
        if filters.user_id:
            tasks = [t for t in tasks if t["user_id"] == filters.user_id]
        if filters.sort_by:
            reverse = filters.order == "desc"
            tasks.sort(key=lambda t: t[filters.sort_by], reverse=reverse)
        if not tasks:
            raise TaskNotFoundError()
        return [TaskResponse(**t) for t in tasks]

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
        self.tasks_db.append(task_db)
        return TaskResponse(**task_db)

    async def service_get_task(self, task_id: int):
        task = None
        for t in self.tasks_db:
            if t["id"] == task_id:
                task = TaskResponse(**t)
        if task is None:
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
        for i, t in enumerate(self.tasks_db):
            if t["id"] == task_id:
                self.tasks_db[i] = task_db
                break
        return TaskResponse(**task_db)
    
    async def service_complete_task(self, task_id: int):
        task_db = await self.service_get_task(task_id)
        task_db = task_db.model_dump()
        if task_db["status"] == "completed":
            raise TaskAlreadyCompletedError()
        task_db["status"] = "completed"
        task_db["updated_at"] = datetime.now().isoformat()
        for i, t in enumerate(self.tasks_db):
            if t["id"] == task_id:
                self.tasks_db[i] = task_db
                break
        return TaskResponse(**task_db)
    
    async def service_assignee_task(self, task_id: int, user_id: int):
        task_db = await self.service_get_task(task_id)
        task_db = task_db.model_dump()
        task_db["user_id"] = user_id
        if task_db["status"] == "pending":
            task_db["status"] = "in_progress"
        task_db["updated_at"] = datetime.now().isoformat()
        for i, t in enumerate(self.tasks_db):
            if t["id"] == task_id:
                self.tasks_db[i] = task_db
                break
        return TaskResponse(**task_db)
    
    async def service_archive_task(self, task_id: int):
        task_db = await self.service_get_task(task_id)
        task_db = task_db.model_dump()
        if task_db["status"] == "archived":
            raise TaskAlreadyArchivedError()
        task_db["status"] = "archived"
        task_db["updated_at"] = datetime.now().isoformat()
        for i, t in enumerate(self.tasks_db):
            if t["id"] == task_id:
                self.tasks_db[i] = task_db
                break
        return TaskResponse(**task_db)
    
    async def service_get_summary(self):
        tasks = self.tasks_db
        summary = {
            "total": len(tasks),
            "pending": sum(1 for t in tasks if t["status"] == "pending"),
            "in_progress": sum(1 for t in tasks if t["status"] == "in_progress"),
            "completed": sum(1 for t in tasks if t["status"] == "completed"),
            "archived": sum(1 for t in tasks if t["status"] == "archived")
        }
        return TasksSummary(**summary)
    
    async def service_export_tasks(self):
        tasks = self.tasks_db
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "title", "description", "status", "user_id", "created_at", "updated_at"])
        for task in tasks:
            writer.writerow([
                task["id"],
                task["title"],
                task["description"] or "",
                task["status"],
                task["user_id"],
                task["created_at"],
                task["updated_at"]
            ])
        
        return output.getvalue()
            