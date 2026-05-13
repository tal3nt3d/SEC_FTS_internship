from tests import *

pytestmark = pytest.mark.repository

class TestTaskRepositoryORM:
    def test_create_task_repository_creates_record_in_db(self, db_session: Session, sample_user, task_repository):
        task_data = TaskCreate(
            title="ORM Test Task",
            description="Testing repository layer"
        )
        
        task = task_repository.create_task(sample_user.id, task_data)
        
        saved_task = db_session.query(Task).filter(Task.id == task.id).first()
        
        assert saved_task is not None
        assert saved_task.title == "ORM Test Task"
        assert saved_task.description == "Testing repository layer"
        assert saved_task.status == "pending"
        assert saved_task.owner_id == sample_user.id
        assert saved_task.created_at is not None
        assert saved_task.updated_at is not None
    
    def test_get_all_tasks_repository_returns_filtered_by_status(self, db_session: Session, sample_user, task_repository):
        
        pending_task = task_repository.create_task(sample_user.id, TaskCreate(title="Pending", description="Desc1"))
        completed_task = task_repository.create_task(sample_user.id, TaskCreate(title="Completed", description="Desc2"))
        task_repository.complete_task(completed_task)
        
        pending_tasks = task_repository.get_all(status="pending")
        
        assert len(pending_tasks) == 1
        assert pending_tasks[0].id == pending_task.id
        assert pending_tasks[0].status == "pending"
    
    def test_get_all_tasks_repository_returns_filtered_by_user(self, db_session: Session, sample_user, sample_assignee, task_repository):
 
        task1 = task_repository.create_task(sample_user.id, TaskCreate(title="User1 Task", description="Desc"))
        task2 = task_repository.create_task(sample_assignee.id, TaskCreate(title="User2 Task", description="Desc"))
        
        user_tasks = task_repository.get_all(user_id=sample_user.id)
        
        assert len(user_tasks) == 1
        assert user_tasks[0].owner_id == sample_user.id
    
    def test_get_all_tasks_repository_sorts_by_created_at(self, db_session: Session, sample_user, task_repository):
 
        task1 = task_repository.create_task(sample_user.id, TaskCreate(title="First", description="Desc"))
        task1.created_at = datetime.now() - timedelta(hours=2)
        task2 = task_repository.create_task(sample_user.id, TaskCreate(title="Second", description="Desc"))
        task2.created_at = datetime.now() - timedelta(hours=1)
        
        tasks_asc = task_repository.get_all(sort_by="created_at", order="asc")
        assert tasks_asc[0].id == task1.id
        assert tasks_asc[1].id == task2.id
        
        tasks_desc = task_repository.get_all(sort_by="created_at", order="desc")
        assert tasks_desc[0].id == task2.id
        assert tasks_desc[1].id == task1.id
    
    def test_update_task_repository_updates_fields(self, db_session: Session, sample_task, task_repository):
        original_updated_at = sample_task.updated_at
        
        update_data = TaskUpdate(
            title="Updated Title",
            description="Updated Description"
        )
        
        updated_task = task_repository.update_task(sample_task, update_data)
        
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Description"
        assert updated_task.updated_at > original_updated_at
    
    def test_complete_task_repository_sets_closed_at(self, db_session: Session, sample_task, task_repository):
        assert sample_task.closed_at is None
        
        completed_task = task_repository.complete_task(sample_task)
        
        assert completed_task.status == "completed"
        assert completed_task.closed_at is not None
        assert isinstance(completed_task.closed_at, datetime)
    
    def test_get_task_with_relationships(self, db_session: Session, sample_task, task_repository):
        
        task = task_repository.get_task(sample_task.id)
        
        assert task.owner is not None
        assert task.owner.id == sample_task.owner_id
        
        assert task.comments is not None
        assert isinstance(task.comments, list)