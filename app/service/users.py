from app.exceptions.errors import UserNotFoundError
from app.schemas.users import UserCreate, UserResponse
from sqlalchemy.orm import Session
from app.repository.users import UserRepository

class UserService:
    def __init__(self, db: Session):
        self.db = UserRepository(db) 
    
    def get_users(self):
        return self.db.get_all()
    
    def get_user_by_id(self, user_id: int):
        user_db = self.db.get_user_by_id(user_id)
        if not user_db:
            raise UserNotFoundError()
        return UserResponse.model_validate(user_db)
    
    def create_user(self, user_data: UserCreate):
        user_db = self.db.create_user(user_data)
        return UserResponse.model_validate(user_db)