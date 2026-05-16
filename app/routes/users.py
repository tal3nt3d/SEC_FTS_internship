"""Tasks router."""

from fastapi import APIRouter, Depends
from app.repository.users import UserRepository
from app.service.users import UserService, UserCreate, UserResponse
from app.schemas.users import LoginRequest, TokenResponse
from app.dependencies.database import get_db
from app.dependencies.users import get_user_service
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

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

@users_router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_username(login_data.username)
    
    if not user or user.password != login_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated"
        )
    
    stub_token = f"stub_{user.id}"
    
    return {"access_token": stub_token, "token_type": "bearer"}