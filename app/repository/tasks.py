from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database.models import Task, TaskHistory
from datetime import datetime
from app.schemas.tasks import TaskCreate, TaskUpdate

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, status: str = None, user_id: int = None, sort_by: str = None, order: str = "asc"):
        sql = """ SELECT * FROM tasks WHERE 1=1 """
        params = {}
        if status:
            sql += """ AND status = :status """
            params["status"] = status
        if user_id:
            sql += """ AND owner_id = :user_id """
            params["user_id"] = user_id
        if sort_by and sort_by in ["created_at", "updated_at"]:
            direction = " DESC " if order == "desc" else " ASC "
            sql += f" ORDER BY {sort_by} {direction}"
        result = self.db.execute(text(sql), params)
        return result.fetchall()

    def create_task(self, owner_id: int, task_data: TaskCreate):
        task = Task(
            owner_id=owner_id,
            title=task_data.title,
            description=task_data.description,
            status="pending",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def get_task(self, task_id: int):
        task = self.db.query(Task).filter(Task.id == task_id).first()
        return task
    
    def complete_task(self, task: Task):
        task.status = "completed"
        task.closed_at = datetime.now()
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def archive_task(self, task: Task):
        task.status = "archived"
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def update_task(self, task: Task, task_data: TaskUpdate):
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.status is not None:
            task.status = task_data.status
        task.updated_at = datetime.now()
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def assign_task(self, task: Task, user_id: int):
        task.assignee_id = user_id
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_task_history(self, task_id: int):
        task_history = self.db.query(TaskHistory).filter(TaskHistory.task_id == task_id).order_by(TaskHistory.changed_at.desc()).all()
        return task_history
    
    def get_summary(self):
        sql = """ SELECT status, COUNT(*) as count FROM tasks GROUP BY status """
        result = self.db.execute(text(sql))
        return result.fetchall()