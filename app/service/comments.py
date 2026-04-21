from storage.comments import comments_db
from storage.tasks import tasks_db
from exceptions.errors import TaskNotFoundError, CommentNotFoundError
from schemas.comments import CommentCreate, CommentResponse
from datetime import datetime

class CommentService:
    def __init__(self):
        self.comments_db = comments_db
        self.tasks_db = tasks_db
    
    async def create_comment(self, task_id: int, comment_data: CommentCreate):
        task_exists = any(t["id"] == task_id for t in self.tasks_db)
        if not task_exists:
            raise TaskNotFoundError()
        comment_dict = CommentResponse(
            id=len(self.comments_db) + 1,
            task_id=task_id,
            text=comment_data.text,
            user_id=comment_data.user_id
        )
        self.comments_db.append(comment_dict.model_dump())
        return comment_dict
    
    async def get_comments(self, task_id: int):
        task_exists = any(t["id"] == task_id for t in self.tasks_db)
        if not task_exists:
            raise TaskNotFoundError()
        comments = [c for c in self.comments_db if c["task_id"] == task_id]
        return [CommentResponse(**c) for c in comments]