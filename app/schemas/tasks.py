from pydantic import BaseModel, Field, ConfigDict, field_validator, ValidationInfo
from typing import Optional, Literal
from enum import Enum
from datetime import datetime

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class TaskModel(BaseModel):
    title: str = Field(min_length=1, max_length = 20)
    description: str = Field(min_length=1, max_length = 200)
    
    model_config = ConfigDict(extra="forbid")

class TaskCreate(TaskModel):
    pass
    
class TaskResponse(TaskModel):
    id: int = Field(..., gt=0)
    status: TaskStatus
    user_id: int = Field(gt=0)
    created_at: datetime
    updated_at: datetime
    
    @field_validator("updated_at")
    @classmethod
    def check_datetime(cls, value: datetime, info: ValidationInfo) -> datetime:
        if value < info.data["created_at"]:
            raise ValueError("updated_at must be greater than created_at")
        return value
        
        
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length = 20)
    description: Optional[str] = Field(None, min_length=1, max_length=200)
    status: Optional[TaskStatus] = None 
    
    model_config = ConfigDict(extra="forbid")

class TaskFilter(BaseModel):
    status: Optional[TaskStatus] = None
    user_id: Optional[int] = None
    sort_by: Optional[Literal["created_at", "updated_at"]] = "created_at"
    order: Optional[Literal["asc", "desc"]] = "desc"
    limit: Optional[int] = Field(default=5, gt=0)
    offset: Optional[int] = Field(default=0, ge=0)
    
    model_config = ConfigDict(extra="forbid")
    
class TasksSummary(BaseModel):
    total: int = 0
    pending: int = 0
    in_progress: int = 0
    completed: int = 0
    archived: int = 0
    
    model_config = ConfigDict(extra="forbid")