from sqlalchemy.orm import Session
from app.database.models import User
from datetime import datetime
from app.schemas.users import UserCreate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(User).all()
    
    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
    
    def create_user(self, user_data: UserCreate):
        user = User(
            username=user_data.username,
            password=user_data.password
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user