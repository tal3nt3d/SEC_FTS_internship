from pydantic import BaseModel, Field, ConfigDict

class CommentModel(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)
    user_id: int = Field(..., gt=0)
    
class CommentCreate(CommentModel):
    pass

class CommentResponse(CommentModel):
    id: int
    task_id: int
    
    model_config = ConfigDict(from_attributes=True)