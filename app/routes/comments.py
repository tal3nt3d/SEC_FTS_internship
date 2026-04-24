"""Comments router."""

from fastapi import APIRouter, Depends, status
from app.service.comments import CommentService
from app.dependencies.comments import get_comment_service
from app.schemas.comments import CommentCreate, CommentResponse

comments_router = APIRouter(prefix="/comments", tags=["comments"])

@comments_router.get("", response_model=list[CommentResponse])
def get_all_comments(comment_service: CommentService = Depends(get_comment_service)):
    return comment_service.get_comments()

@comments_router.post("/{task_id}", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(task_id: int, comment: CommentCreate, comment_service: CommentService = Depends(get_comment_service)):
    return comment_service.create_comment(task_id, comment)

@comments_router.get("/{task_id}", response_model=list[CommentResponse])
def get_comments_by_task(task_id: int, comment_service: CommentService = Depends(get_comment_service)):
    return comment_service.get_comments_by_task_id(task_id)