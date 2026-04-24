from app.service.users import UserService
from .database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)
