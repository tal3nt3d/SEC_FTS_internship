from app.exceptions.errors import TaskNotFoundError, CommentNotFoundError
from app.schemas.comments import CommentCreate, CommentResponse
from datetime import datetime
from sqlalchemy.orm import Session
from app.repository.comments import CommentRepository

class CommentService:
    def __init__(self, db: Session):
        self.repo = CommentRepository(db)
    
    def get_comments(self):
        comments = self.repo.get_all()
        return comments
    
    def get_comments_by_task_id(self, task_id: int):
        comment = self.repo.get_comments(task_id)
        if not comment:
            raise CommentNotFoundError()
        return comment
    
    def create_comment(self, task_id: int, comment_data: CommentCreate):
        comment = self.repo.create_comment(task_id, comment_data)
        return comment
