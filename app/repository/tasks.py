from sqlalchemy.orm import Session
from app.database.models import Task
from datetime import datetime

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, status: str = None, user_id: int = None, sort_by: str = None, order: str = "asc"):
        query = self.db.query(Task)
        
        if status:
            query = query.filter(Task.status == status)
        if user_id:
            query = query.filter(Task.owner_id == user_id)
            
        if sort_by and hasattr(Task, sort_by):
            column = getattr(Task, sort_by)
            query = query.order_by(column.desc() if order == "desc" else column.asc())
            
        return query.all()
    
    def create_task(self, owner_id: int, title: str, description: str):
        task = Task(
            owner_id=owner_id,
            title=title,
            description=description,
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
    
    def complete_task(self, task_id: int):
        task = self.get_task(task_id)
        task.status = "completed"
        task.closed_at = datetime.now()
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def archive_task(self, task_id: int):
        task = self.get_task(task_id)
        task.status = "archived"
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def update_task(self, task_id, task_data):
        task = self.get_task(task_id)
        task.title = task_data.title
        task.description = task_data.description
        task.status = task_data.status
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def assign_task(self, task_id, user_id):
        task = self.get_task(task_id)
        task.assignee_id = user_id
        self.db.commit()
        self.db.refresh(task)
        return task