from sqlalchemy.orm import Session
from app.database.models import Comment
from datetime import datetime

class CommentRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def get_all(self):
        return self.db.query(Comment).all()
    
    def get_comments(self, task_id: int):
        comments = self.db.query(Comment).filter(Comment.task_id == task_id)
        return comments
    
    def create_comment(self, task_id: int, content: str, user_id: int):
        comment = Comment(
            content=content,
            task_id=task_id,
            user_id=user_id
        )
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment