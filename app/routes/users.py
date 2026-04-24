"""Tasks router."""

from fastapi import APIRouter, Depends
from app.repository.users import UserRepository
from app.service.users import UserService, UserCreate, UserResponse
from app.dependencies.users import get_user_service


users_router = APIRouter(prefix="/users", tags=["users"])

@users_router.get("", response_model=list[UserResponse])
def read_users(user_service: UserService = Depends(get_user_service)):
    return user_service.get_users()

@users_router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    return user_service.get_user_by_id(user_id)

@users_router.post("", response_model=UserResponse)
def create_user(user_data: UserCreate, user_service: UserService = Depends(get_user_service)):
    return user_service.create_user(user_data)