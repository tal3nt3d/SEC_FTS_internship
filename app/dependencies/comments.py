from app.service.comments import CommentService
from .database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

def get_comment_service(db: Session = Depends(get_db)) -> CommentService:
    return CommentService(db)
