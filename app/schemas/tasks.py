from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal
from enum import Enum
from datetime import datetime

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class TaskModel(BaseModel):
    title: str = Field(max_length = 20)
    description: str = Field(max_length = 200)

class TaskCreate(TaskModel):
    pass
    
class TaskResponse(TaskModel):
    id: int = Field(..., gt=0)
    status: TaskStatus
    user_id: int = Field(gt=0)
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
        
class TaskUpdate(TaskModel):
    title: Optional[str] = Field(None, max_length = 20)
    description: Optional[str] = Field(None, max_length=200)
    status: Optional[TaskStatus] = None 
    
    model_config = ConfigDict(extra="forbid")

class TaskFilter(BaseModel):
    status: Optional[TaskStatus] = None
    user_id: Optional[int] = None
    sort_by: Optional[Literal["created_at", "updated_at"]] = "created_at"
    order: Optional[Literal["asc", "desc"]] = "desc"
    
class TasksSummary(BaseModel):
    total: int = 0
    pending: int = 0
    in_progress: int = 0
    completed: int = 0
    archived: int = 0