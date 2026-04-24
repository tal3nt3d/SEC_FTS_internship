from app.exceptions.errors import TaskNotFoundError, TaskAlreadyCompletedError, TaskAlreadyArchivedError
from app.schemas.tasks import TaskCreate, TaskResponse, TaskUpdate, TaskFilter, TasksSummary
from datetime import datetime
import csv
from io import StringIO
from sqlalchemy.orm import Session
from app.repository.tasks import TaskRepository

class TaskService:
    def __init__(self, db: Session):
        self.repo = TaskRepository(db)
    
    def get_tasks(self, filters: TaskFilter):
        tasks = self.repo.get_all(
            status=filters.status, 
            user_id=filters.user_id, 
            sort_by=filters.sort_by, 
            order=filters.order
        )
        start = filters.offset
        end = start + filters.limit
        paginated_tasks = tasks[start:end]
        return paginated_tasks

    def create_task(self, owner_id: int, task_data: TaskCreate):
        task = self.repo.create_task(owner_id, task_data.title, task_data.description)
        return TaskResponse.model_validate(task)

    def get_task_by_id(self, task_id: int):
        task = self.repo.get_task(task_id)
        if not task:
            raise TaskNotFoundError()
        return TaskResponse.model_validate(task)
    
    def update_task(self, task_id: int, task_data: TaskUpdate):
        task = self.repo.get_task(task_id)
        if task.status == "completed": # правильно ли, что мы не даём изменять уже завершённые задачи?
            raise TaskAlreadyCompletedError()
        task = self.repo.update_task(task_id, task_data)
        return TaskResponse.model_validate(task)
    
    def complete_task(self, task_id: int):
        task = self.get_task_by_id(task_id)
        if task.status == "completed": # --//--
            raise TaskAlreadyCompletedError()
        task = self.repo.complete_task(task_id)
        return TaskResponse.model_validate(task)
    
    def archive_task(self, task_id: int):
        task = self.get_task_by_id(task_id)
        if task.status == "completed": # --//--
            raise TaskAlreadyCompletedError()
        if task.status == "archived":
            raise TaskAlreadyArchivedError()
        task = self.repo.archive_task(task_id)
        return TaskResponse.model_validate(task)
    
    def assignee_task(self, task_id: int, user_id: int):
        task = self.get_task_by_id(task_id)
        if task.status == "completed": # --//--
            raise TaskAlreadyCompletedError()
        task = self.repo.assign_task(task_id, user_id)
        return TaskResponse.model_validate(task)
    
    def get_summary(self):
        tasks = self.get_tasks(TaskFilter())
        summary = TasksSummary(
            total=len(tasks),
            pending=sum(1 for t in tasks if t.status == "pending"),
            in_progress=sum(1 for t in tasks if t.status == "in_progress"),
            completed=sum(1 for t in tasks if t.status == "completed"),
            archived=sum(1 for t in tasks if t.status == "archived")
            
        )
        return summary
    
    def export_tasks(self):
        tasks = self.get_tasks(TaskFilter())
        output = StringIO()
        writer = csv.writer(output, delimiter=',')
        writer.writerow(["id", "title", "description", "status","created_at", "updated_at", "closed_at", "owner_id", "assignee_id"])
        for task in tasks:
            writer.writerow([
                task.id,
                task.title,
                task.description,
                task.status,
                task.created_at,
                task.updated_at,
                task.closed_at or "",
                task.owner_id,
                task.assignee_id or ""
            ])
        
        return output.getvalue()
            