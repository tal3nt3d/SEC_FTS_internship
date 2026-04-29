from app.service.tasks import TaskService
from .database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(db)
