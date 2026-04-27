from app.exceptions.errors import TaskNotFoundError, TaskAlreadyCompletedError, TaskAlreadyArchivedError
from app.schemas.tasks import TaskCreate, TaskResponse, TaskUpdate, TaskFilter, TasksSummary, TaskHistoryResponse
from datetime import datetime
import csv
from io import StringIO
from sqlalchemy.orm import Session
from app.repository.tasks import TaskRepository
from app.database.models import TaskHistory

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
        task = self.repo.create_task(owner_id, task_data)
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
        changes = {}
        if task_data.title is not None:
            changes["title"] = (task.title, task_data.title)
        if task_data.description is not None:
            changes["description"] = (task.description, task_data.description)
        if task_data.status is not None:
            changes["status"] = (task.status, task_data.status)
        task = self.repo.update_task(task_id, task_data)
        self.save_history(task_id, changes)
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

    def save_history(self, task_id: int, changes: dict):
        for field, (old, new) in changes.items():
            if old != new:
                history = TaskHistory(
                    task_id=task_id,
                    field_name=field,
                    old_value=str(old) if old is not None else None,
                    new_value=str(new) if new is not None else None,
                )
                self.repo.db.add(history)
        
        self.repo.db.commit()
        
    from app.schemas.tasks import TaskHistoryResponse

    def get_task_history(self, task_id: int):
        history = self.repo.get_task_history(task_id)
        if history is None:
            raise TaskNotFoundError()
        return [TaskHistoryResponse.model_validate(h) for h in history]