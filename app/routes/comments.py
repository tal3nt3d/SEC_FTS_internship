"""Tasks router."""

from fastapi import APIRouter
from service.comments import get_comments

comments_router = APIRouter(prefix="/comments", tags=["comments"])

@comments_router.get("")
async def return_comments():
    comments = await get_comments()
    return comments
