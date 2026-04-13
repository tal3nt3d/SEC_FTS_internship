"""Tasks router."""

from fastapi import APIRouter
from service.users import get_users

users_router = APIRouter(prefix="/users", tags=["users"])

@users_router.get("")
async def return_users():
    users = await get_users()
    return users
