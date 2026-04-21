from storage.tasks import tasks_db
from exceptions.errors import TaskNotFoundError, TaskAlreadyCompletedError, TaskAlreadyArchivedError
from schemas.tasks import TaskCreate, TaskResponse, TaskUpdate, TaskFilter, TasksSummary
from datetime import datetime
import csv
from io import StringIO

class TaskService:
    def __init__(self):
        self.tasks_db : list = tasks_db
    
    async def get_tasks(self, filters: TaskFilter):
        tasks = self.tasks_db.copy()
        if filters.status: 
            tasks = [t for t in tasks if t["status"] == filters.status]
        if filters.user_id:
            tasks = [t for t in tasks if t["user_id"] == filters.user_id]
        if filters.sort_by:
            reverse = filters.order == "desc"
            tasks.sort(key=lambda t: t[filters.sort_by], reverse=reverse)
        start = filters.offset
        end = start + filters.limit
        tasks = tasks[start:end] #что лучше: вернуть пустой или прокинуть ошибку?
        if not tasks:
            raise TaskNotFoundError()
        return [TaskResponse(**t) for t in tasks]

    async def create_task(self, user_id: int, task_data: TaskCreate):
        task_db = TaskResponse(
            id=len(self.tasks_db) + 1,
            status="pending",
            user_id=user_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            title=task_data.title,
            description=task_data.description
        )
        self.tasks_db.append(task_db.model_dump())
        print(self.tasks_db)
        return task_db

    async def get_task(self, task_id: int):
        task = None
        for t in self.tasks_db:
            if t["id"] == task_id:
                task = TaskResponse(**t)
        if task is None:
            raise TaskNotFoundError()
        return task
    
    async def change_db(self, task_id: int, task_db: dict):
        for i, t in enumerate(self.tasks_db):
            if t["id"] == task_id:
                self.tasks_db[i] = task_db
                break
    
    async def update_task(self, task_id: int, task_data: TaskUpdate):
        task_db = await self.get_task(task_id)
        task_db = task_db.model_dump()
        if task_data.title:
            task_db["title"] = task_data.title
        if task_data.description:
            task_db["description"] = task_data.description
        if task_data.status:
            task_db["status"] = task_data.status
        task_db["updated_at"] = datetime.now()
        await self.change_db(task_id, task_db)
        return TaskResponse(**task_db)
    
    async def complete_task(self, task_id: int):
        task_db = await self.get_task(task_id)
        task_db = task_db.model_dump()
        if task_db["status"] == "completed":
            raise TaskAlreadyCompletedError()
        task_db["status"] = "completed"
        task_db["updated_at"] = datetime.now()
        await self.change_db(task_id, task_db)
        return TaskResponse(**task_db)
    
    async def assignee_task(self, task_id: int, user_id: int):
        task_db = await self.get_task(task_id)
        task_db = task_db.model_dump()
        task_db["user_id"] = user_id
        if task_db["status"] == "pending":
            task_db["status"] = "in_progress"
        task_db["updated_at"] = datetime.now()
        await self.change_db(task_id, task_db)
        return TaskResponse(**task_db)
    
    async def archive_task(self, task_id: int):
        task_db = await self.get_task(task_id)
        task_db = task_db.model_dump()
        if task_db["status"] == "archived":
            raise TaskAlreadyArchivedError()
        task_db["status"] = "archived"
        task_db["updated_at"] = datetime.now()
        await self.change_db(task_id, task_db)
        return TaskResponse(**task_db)
    
    async def get_summary(self):
        tasks = self.tasks_db
        summary = TasksSummary(
            total=len(tasks),
            pending=sum(1 for t in tasks if t["status"] == "pending"),
            in_progress=sum(1 for t in tasks if t["status"] == "in_progress"),
            completed=sum(1 for t in tasks if t["status"] == "completed"),
            archived=sum(1 for t in tasks if t["status"] == "archived")
            
        )
        return summary
    
    async def export_tasks(self):
        tasks = self.tasks_db
        output = StringIO()
        writer = csv.writer(output, delimiter=',')
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
            