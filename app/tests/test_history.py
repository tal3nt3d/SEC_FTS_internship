from tests import *

pytestmark = pytest.mark.history

class TestTaskHistoryRecording:
    def test_update_task_title_creates_history_record(self, db_session: Session, sample_task):
        service = TaskService(db_session)
        
        history_before = db_session.query(TaskHistory).filter(
            TaskHistory.task_id == sample_task.id
        ).all()
        assert len(history_before) == 0
        
        update_data = TaskUpdate(title="New Updated Title")
        service.update_task(sample_task.id, update_data)
        
        history_after = db_session.query(TaskHistory).filter(
            TaskHistory.task_id == sample_task.id
        ).all()
        
        assert len(history_after) == 1
        history_record = history_after[0]
        
        assert history_record.task_id == sample_task.id
        assert history_record.field_name == "title"
        assert history_record.old_value == "Test Task"
        assert history_record.new_value == sample_task.title
        assert history_record.changed_at is not None
    
    def test_update_task_description_creates_history_record(self, db_session: Session, sample_task):
        service = TaskService(db_session)
        original_description = sample_task.description
        
        update_data = TaskUpdate(description="Brand new description")
        service.update_task(sample_task.id, update_data)
        
        history = db_session.query(TaskHistory).filter(
            TaskHistory.task_id == sample_task.id,
            TaskHistory.field_name == "description"
        ).first()
        
        assert history is not None
        assert history.old_value == original_description
        assert history.new_value == "Brand new description"
    
    def test_update_task_status_creates_history_record(self, db_session: Session, sample_task):
        service = TaskService(db_session)
        
        update_data = TaskUpdate(status="in_progress")
        service.update_task(sample_task.id, update_data)
        
        history = db_session.query(TaskHistory).filter(
            TaskHistory.task_id == sample_task.id,
            TaskHistory.field_name == "status"
        ).first()
        
        assert history is not None
        assert history.old_value == "pending"
        assert "in_progress" in history.new_value.lower()
    
    def test_update_multiple_fields_creates_multiple_history_records(self, db_session: Session, sample_task):
        service = TaskService(db_session)
        original_title = sample_task.title
        original_description = sample_task.description
        
        update_data = TaskUpdate(
            title="New Title",
            description="New Description"
        )
        service.update_task(sample_task.id, update_data)
        
        history_records = db_session.query(TaskHistory).filter(
            TaskHistory.task_id == sample_task.id
        ).all()
        
        assert len(history_records) == 2
        
        title_record = next((h for h in history_records if h.field_name == "title"), None)
        desc_record = next((h for h in history_records if h.field_name == "description"), None)
        
        assert title_record is not None
        assert title_record.old_value == original_title
        assert title_record.new_value == "New Title"
        
        assert desc_record is not None
        assert desc_record.old_value == original_description
        assert desc_record.new_value == "New Description"
    
    def test_history_records_are_ordered_by_changed_at(self, db_session: Session, sample_task):
        service = TaskService(db_session)
        
        service.update_task(sample_task.id, TaskUpdate(title="Title v1"))
        service.update_task(sample_task.id, TaskUpdate(description="Desc v1"))
        service.update_task(sample_task.id, TaskUpdate(title="Title v2"))
        
        history = db_session.query(TaskHistory).filter(
            TaskHistory.task_id == sample_task.id
        ).order_by(TaskHistory.changed_at.desc()).all()
        
        assert len(history) == 3
        assert history[0].new_value == "Title v2"
    
    def test_no_history_record_when_value_unchanged(self, db_session: Session, sample_task):
        service = TaskService(db_session)
        original_title = sample_task.title
        
        update_data = TaskUpdate(title=original_title)
        service.update_task(sample_task.id, update_data)
        
        history = db_session.query(TaskHistory).filter(
            TaskHistory.task_id == sample_task.id
        ).all()
        
        assert len(history) == 0
    
    def test_history_contains_none_values_for_optional_fields(self, db_session: Session, sample_task):
        service = TaskService(db_session)

        from app.database.models import TaskHistory
        
        history_record = TaskHistory(
            task_id=sample_task.id,
            field_name="assignee_id",
            old_value=None,
            new_value="5"
        )
        db_session.add(history_record)
        db_session.commit()
        
        saved = db_session.query(TaskHistory).filter(
            TaskHistory.task_id == sample_task.id
        ).first()
        
        assert saved.old_value is None
        assert saved.new_value == "5"
    
    
class TestTaskHistoryEndpoint:
    def test_get_task_history_returns_records(self, db_session: Session, client, sample_task):
        service = TaskService(db_session)
        
        service.update_task(sample_task.id, TaskUpdate(title="First Update"))
        service.update_task(sample_task.id, TaskUpdate(description="Second Update"))
        
        response = client.get(f"/tasks/{sample_task.id}/history")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) == 2
        
        for record in data:
            assert "id" in record
            assert "task_id" in record
            assert "field_name" in record
            assert "old_value" in record
            assert "new_value" in record
            assert "changed_at" in record
            assert record["task_id"] == sample_task.id
    
    def test_get_task_history_empty(self, client, sample_task):
        response = client.get(f"/tasks/{sample_task.id}/history")
        
        assert response.status_code == 404