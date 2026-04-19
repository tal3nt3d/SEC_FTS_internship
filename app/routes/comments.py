"""Comments router."""

from fastapi import APIRouter, Depends
from service.comments import CommentService
from dependencies.comments import get_comment_service
from schemas.comments import CommentCreate, CommentResponse

comments_router = APIRouter(prefix="/tasks", tags=["comments"])

@comments_router.post("/{task_id}/comments", response_model=CommentResponse, status_code=201)
async def create_comment(task_id: int, comment: CommentCreate, comment_service: CommentService = Depends(get_comment_service)):
    return await comment_service.service_create_comment(task_id, comment)

@comments_router.get("/{task_id}/comments", response_model=list[CommentResponse])
async def get_comments(task_id: int, comment_service: CommentService = Depends(get_comment_service)):
    return await comment_service.service_get_comments(task_id)