from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, CheckConstraint, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    closed_at = Column(DateTime, nullable=True)
    
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    owner = relationship("User", foreign_keys="Task.owner_id", back_populates="owned_tasks")
    assignee = relationship("User", foreign_keys="Task.assignee_id", back_populates="assigned_tasks")
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")
    history = relationship("TaskHistory", back_populates="task", cascade="all, delete-orphan")
    
    __table_args__ = (
        CheckConstraint("status IN ('pending', 'in_progress', 'archived', 'completed')", name="check_status"),
        
        Index('idx_tasks_status', 'status'),  # Фильтр по статусу
        Index('idx_tasks_owner_id', 'owner_id'),  # Фильтр по владельцу
        Index('idx_tasks_assignee_id', 'assignee_id'),  # Фильтр по исполнителю
        
        Index('idx_tasks_owner_status', 'owner_id', 'status'),  # WHERE owner_id = ? AND status = ?
        Index('idx_tasks_assignee_status', 'assignee_id', 'status'),  # WHERE assignee_id = ? AND status = ?
        
        Index('idx_tasks_created_at', 'created_at'),  # ORDER BY created_at
        Index('idx_tasks_updated_at', 'updated_at'),  # ORDER BY updated_at
        
        Index('idx_tasks_status_created', 'status', 'created_at'),  # WHERE status = ? ORDER BY created_at
        Index('idx_tasks_owner_created', 'owner_id', 'created_at'),  # WHERE owner_id = ? ORDER BY created_at
    )
    
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    task = relationship("Task", back_populates="comments")
    user = relationship("User", back_populates="comments")
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    owned_tasks = relationship("Task", foreign_keys="Task.owner_id", back_populates="owner", cascade="all, delete-orphan")
    assigned_tasks = relationship("Task", foreign_keys="Task.assignee_id", back_populates="assignee")
    
class TaskHistory(Base):
    __tablename__ = "task_history"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    field_name = Column(String, nullable=False)
    old_value = Column(String, nullable=True)
    new_value = Column(String, nullable=True)
    changed_at = Column(DateTime, nullable=False, default=datetime.now)
    changed_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    task = relationship("Task", back_populates="history")