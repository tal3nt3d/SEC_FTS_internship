import os
import sys
import pytest
from datetime import datetime, timedelta
from pathlib import Path
from typing import Generator, List, Dict, Any
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

os.environ["APP_ENV"] = "test"

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app
from app.database.database import Base
from app.service.tasks import TaskService

TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(engine) -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection, autocommit=False, autoflush=False)()

    from app.dependencies.tasks import get_task_service
    
    def override_get_task_service():
        return TaskService(session)
    
    app.dependency_overrides[get_task_service] = override_get_task_service

    yield session

    app.dependency_overrides.clear()
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session) -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def sample_user(db_session: Session):
    from app.database.models import User
    
    user = User(username="test_user", password="hashed_password")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def sample_assignee(db_session: Session):
    from app.database.models import User
    
    user = User(username="assignee_user", password="hashed_password")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def multiple_users(db_session: Session) -> List[Dict[str, Any]]:
    from app.database.models import User
    
    users = []
    for i in range(3):
        user = User(username=f"user_{i}", password=f"pass_{i}")
        db_session.add(user)
        users.append({"id": None, "username": f"user_{i}"})
    
    db_session.commit()
    
    for i, user in enumerate(users):
        db_user = db_session.query(User).filter(User.username == f"user_{i}").first()
        users[i]["id"] = db_user.id
    
    return users

@pytest.fixture
def sample_task(db_session: Session, sample_user):
    from app.database.models import Task
    
    task = Task(
        title="Test Task",
        description="Test Description",
        status="pending",
        owner_id=sample_user.id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task


@pytest.fixture
def sample_completed_task(db_session: Session, sample_user):
    from app.database.models import Task
    
    task = Task(
        title="Completed Task",
        description="This task is already done",
        status="completed",
        owner_id=sample_user.id,
        created_at=datetime.now() - timedelta(days=1),
        updated_at=datetime.now(),
        closed_at=datetime.now()
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task


@pytest.fixture
def sample_archived_task(db_session: Session, sample_user):
    from app.database.models import Task
    
    task = Task(
        title="Archived Task",
        description="This task is archived",
        status="archived",
        owner_id=sample_user.id,
        created_at=datetime.now() - timedelta(days=2),
        updated_at=datetime.now()
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task


@pytest.fixture
def sample_in_progress_task(db_session: Session, sample_user):
    from app.database.models import Task
    
    task = Task(
        title="In Progress Task",
        description="Task being worked on",
        status="in_progress",
        owner_id=sample_user.id,
        created_at=datetime.now() - timedelta(hours=5),
        updated_at=datetime.now()
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task


@pytest.fixture
def multiple_tasks(db_session: Session, sample_user) -> List[Dict[str, Any]]:
    from app.database.models import Task
    
    tasks_data = [
        ("Task 1", "Description 1", "pending", sample_user.id),
        ("Task 2", "Description 2", "in_progress", sample_user.id),
        ("Task 3", "Description 3", "completed", sample_user.id),
        ("Task 4", "Description 4", "archived", sample_user.id),
        ("Task 5", "Description 5", "pending", sample_user.id),
    ]
    
    tasks = []
    for title, desc, status, owner_id in tasks_data:
        task = Task(
            title=title,
            description=desc,
            status=status,
            owner_id=owner_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db_session.add(task)
        tasks.append({"title": title, "status": status})
    
    db_session.commit()
    
    for task_dict in tasks:
        task = db_session.query(Task).filter(Task.title == task_dict["title"]).first()
        task_dict["id"] = task.id
    
    return tasks

@pytest.fixture
def task_service(db_session: Session) -> TaskService:
    return TaskService(db_session)


@pytest.fixture
def task_service_with_data(db_session: Session, sample_user, multiple_tasks) -> TaskService:
    service = TaskService(db_session)
    return service
