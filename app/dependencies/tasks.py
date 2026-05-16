from app.service.tasks import TaskService
from .database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from app.dependencies.auth import get_current_user, CurrentUser

def get_task_service(db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)) -> TaskService:
    return TaskService(db, current_user)
