from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

my_config = ConfigDict(extra="forbid", from_attributes=True)

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"
    
class UserModel(BaseModel):
    username: str = Field(min_length=1, max_length = 20)
    password: str = Field(min_length=1, max_length = 20)
    
    model_config = my_config

class UserCreate(UserModel):
    pass
    
class UserResponse(UserModel):
    id: int = Field(..., gt=0)
    role: UserRole = Field(default=UserRole.USER)
    is_active: bool = Field(default=True)
    
    model_config = my_config
    
class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length = 20)
    password: str = Field(min_length=1, max_length = 20)

class TokenResponse(BaseModel):
    access_token: str = Field(..., min_length=1)
    token_type: str = "bearer"