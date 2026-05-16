from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from app.dependencies.database import get_db
from app.repository.users import UserRepository
from app.database.models import User
from app.exceptions.errors import UserNotFoundError

security = HTTPBearer(auto_error=False)

async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security), db: Session = Depends(get_db)) -> User:
    user_id = None
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Provide Authorization: Bearer stub_<id>",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = credentials.credentials
    if not token.startswith("stub_"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format. Use 'stub_<user_id>'",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        user_id = int(token.split("_")[1])
    except (IndexError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid stub token format. Use 'stub_<user_id>'",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_id(user_id)
    
    if user is None:
        raise UserNotFoundError
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated"
        )
    
    return user

CurrentUser = User