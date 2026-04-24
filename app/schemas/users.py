from pydantic import BaseModel, Field, ConfigDict

my_config = ConfigDict(extra="forbid", from_attributes=True)

class UserModel(BaseModel):
    username: str = Field(min_length=1, max_length = 20)
    password: str = Field(min_length=1, max_length = 20)
    
    model_config = my_config

class UserCreate(UserModel):
    pass
    
class UserResponse(UserModel):
    id: int = Field(..., gt=0)
    
    model_config = my_config