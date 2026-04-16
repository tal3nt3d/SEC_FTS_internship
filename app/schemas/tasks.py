from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str
    
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    user_id: int
    created_at: str
    updated_at: str
    
    class Config:
        orm_mode = True
        
class TaskUpdate(BaseModel):
    title: str
    description: str
    status: str
