from sqlalchemy.orm import Session
from app.database.models import User
from datetime import datetime

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(User).all()
    
    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
    
    def create_user(self, name: str, password: str):
        user = User(
            username=name,
            password=password
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user