from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    closed_at = Column(DateTime, nullable=True)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    owner = relationship("User", foreign_keys="Task.owner_id", back_populates="owned_tasks")
    assignee = relationship("User", foreign_keys="Task.assignee_id", back_populates="assigned_tasks")
    comments = relationship("Comment", back_populates="task")
    history = relationship("TaskHistory", back_populates="task")
    
    __table_args__ = (
        CheckConstraint("status IN ('pending', 'in_progress', 'archived', 'completed')", name="check_status"),
    )
    
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    content = Column(String)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    task = relationship("Task", back_populates="comments")
    user = relationship("User", back_populates="comments")
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    
    comments = relationship("Comment", back_populates="user")
    owned_tasks = relationship("Task", foreign_keys="Task.owner_id", back_populates="owner")
    assigned_tasks = relationship("Task", foreign_keys="Task.assignee_id", back_populates="assignee")
    
class TaskHistory(Base):
    __tablename__ = "task_history"
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    field_name = Column(String)
    old_value = Column(String, nullable=True)
    new_value = Column(String, nullable=True)
    changed_at = Column(DateTime, default=datetime.now)
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    task = relationship("Task", back_populates="history")