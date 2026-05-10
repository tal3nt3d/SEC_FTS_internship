from sqlalchemy import Integer, String, ForeignKey, DateTime, CheckConstraint, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from .database import Base
from typing import Optional, List

class Task(Base):
    __tablename__ = "tasks"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    assignee_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    owner: Mapped["User"] = relationship("User", foreign_keys="Task.owner_id", back_populates="owned_tasks")
    assignee: Mapped[Optional["User"]] = relationship("User", foreign_keys="Task.assignee_id", back_populates="assigned_tasks")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="task", cascade="all, delete-orphan")
    history: Mapped[List["TaskHistory"]] = relationship("TaskHistory", back_populates="task", cascade="all, delete-orphan")
    
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
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    content: Mapped[str] = mapped_column(String, nullable=False)
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    task: Mapped["Task"] = relationship("Task", back_populates="comments")
    user: Mapped["User"] = relationship("User", back_populates="comments")


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    owned_tasks: Mapped[List["Task"]] = relationship("Task", foreign_keys="Task.owner_id", back_populates="owner", cascade="all, delete-orphan")
    assigned_tasks: Mapped[List["Task"]] = relationship("Task", foreign_keys="Task.assignee_id", back_populates="assignee")


class TaskHistory(Base):
    __tablename__ = "task_history"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    field_name: Mapped[str] = mapped_column(String, nullable=False)
    old_value: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    new_value: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    changed_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    changed_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    task: Mapped["Task"] = relationship("Task", back_populates="history")