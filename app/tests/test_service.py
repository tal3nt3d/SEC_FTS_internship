from tests import *

pytestmark = pytest.mark.service

class TestTaskServiceIntegration:
    def test_service_create_task_returns_valid_response(self, db_session: Session, sample_user, task_service):
        task_data = TaskCreate(
            title="Service Test Task",
            description="Testing service layer"
        )
        
        result = task_service.create_task(sample_user.id, task_data)
        
        assert result.id is not None
        assert result.title == "Service Test Task"
        assert result.description == "Testing service layer"
        assert result.status == "pending"
        assert result.owner_id == sample_user.id
        assert result.created_at is not None
    
    def test_service_create_task_with_nonexistent_user_raises_error(self, db_session: Session, task_service):
        task_data = TaskCreate(title="Test", description="Test")
        
        with pytest.raises(UserNotFoundError) as exc_info:
            task_service.create_task(99999, task_data)
        
        assert exc_info.value.status_code == 404
        assert "User not found" in str(exc_info.value.detail)
    
    def test_service_get_task_by_id_returns_correct_task(self, db_session: Session, sample_task, task_service):
        
        result = task_service.get_task_by_id(sample_task.id)
        
        assert result.id == sample_task.id
        assert result.title == sample_task.title
    
    def test_service_get_nonexistent_task_raises_error(self, db_session: Session, task_service):
        
        with pytest.raises(TaskNotFoundError) as exc_info:
            task_service.get_task_by_id(99999)
        
        assert exc_info.value.status_code == 404
        assert "Task not found" in str(exc_info.value.detail)
    
    def test_service_complete_task_changes_status(self, db_session: Session, sample_task, task_service):
        assert sample_task.status == "pending"
        
        result = task_service.complete_task(sample_task.id)
        
        assert result.status == "completed"
        assert result.closed_at is not None
    
    def test_service_complete_already_completed_task_raises_error(self, db_session: Session, sample_completed_task, task_service):
        
        with pytest.raises(TaskAlreadyCompletedError) as exc_info:
            task_service.complete_task(sample_completed_task.id)
        
        assert exc_info.value.status_code == 409
        assert "already completed" in str(exc_info.value.detail)
    
    def test_service_update_task_changes_multiple_fields(self, db_session: Session, sample_task, task_service):
        update_data = TaskUpdate(
            title="New Title",
            description="New Description",
            status="in_progress"
        )
        
        result = task_service.update_task(sample_task.id, update_data)
        
        assert result.title == "New Title"
        assert result.description == "New Description"
        assert result.status == "in_progress"
    
    def test_service_assign_task_changes_assignee(self, db_session: Session, sample_task, sample_assignee, task_service):
        assert sample_task.assignee_id is None
        
        result = task_service.assignee_task(sample_task.id, sample_assignee.id)
        
        assert result.assignee_id == sample_assignee.id
    
    def test_service_archive_task_changes_status_to_archived(self, db_session: Session, sample_task, task_service):
        
        result = task_service.archive_task(sample_task.id)
        
        assert result.status == "archived"
    
    def test_service_get_summary_returns_counts(self, db_session: Session, sample_user, task_service):
        
        task_service.create_task(sample_user.id, TaskCreate(title="Task1", description="Desc1"))
        task2 = task_service.create_task(sample_user.id, TaskCreate(title="Task2", description="Desc2"))
        task_service.complete_task(task2.id)
        task3 = task_service.create_task(sample_user.id, TaskCreate(title="Task3", description="Desc3"))
        task_service.archive_task(task3.id)
        
        summary = task_service.get_summary()
        
        assert summary.total == 3
        assert summary.pending == 1
        assert summary.completed == 1
        assert summary.archived == 1
        assert summary.in_progress == 0
    
    def test_service_get_tasks_with_pagination(self, db_session: Session, sample_user, task_service):
        
        for i in range(10):
            task_service.create_task(sample_user.id, TaskCreate(title=f"Task{i}", description="Desc"))
        
        filter1 = TaskFilter(limit=3, offset=0)
        page1 = task_service.get_tasks(filter1)
        assert len(page1) == 3
        
        filter2 = TaskFilter(limit=3, offset=3)
        page2 = task_service.get_tasks(filter2)
        assert len(page2) == 3
        
        assert page1[0].id != page2[0].id