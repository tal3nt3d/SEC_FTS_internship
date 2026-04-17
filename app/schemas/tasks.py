from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from enum import Enum
from datetime import datetime

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

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
