from tests import *

pytestmark = pytest.mark.validation

class TestValidationErrors:
    def test_create_task_missing_title(self, client: TestClient, sample_user):
        response = client.post(
            "/tasks",
            params={"owner_id": sample_user.id},
            json={
                "description": "Description without title"
            }
        )
        
        assert response.status_code == 422
        error_data = response.json()
        assert "details" in error_data
        
        errors = error_data["details"]
        field_errors = [e for e in errors if "Field" in str(e)]
        assert len(field_errors) > 0
    
    def test_create_task_missing_description(self, client: TestClient, sample_user):
        response = client.post(
            "/tasks",
            params={"owner_id": sample_user.id},
            json={
                "title": "Title without description"
            }
        )
        
        assert response.status_code == 422
        error_data = response.json()
        assert "details" in error_data
        
        errors = error_data["details"]
        field_errors = [e for e in errors if "character" in str(e)]
        assert len(field_errors) > 0
    
    def test_create_task_title_none(self, client: TestClient, sample_user):
        response = client.post(
            "/tasks",
            params={"owner_id": sample_user.id},
            json={
                "title": None,
                "description": "Valid description"
            }
        )
        
        assert response.status_code == 422
        error_data = response.json()
        assert "details" in error_data
    
    def test_create_task_empty_json(self, client: TestClient, sample_user):
        response = client.post(
            "/tasks",
            params={"owner_id": sample_user.id},
            json={}
        )
        
        assert response.status_code == 422
    
    def test_update_task_nonexistent_field(self, client: TestClient, sample_task):
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={
                "title": "Updated title",
                "nonexistent_field": "should be forbidden"
            }
        )
        
        assert response.status_code == 422
        error_data = response.json()
        assert "details" in error_data
    
    def test_update_task_invalid_status_value(self, client: TestClient, sample_task):
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={
                "status": "invalid_status_123"
            }
        )
        
        assert response.status_code == 422
        error_data = response.json()
        assert "details" in error_data
    
    def test_get_task_with_string_id(self, client: TestClient):
        response = client.get("/tasks/abc")
        
        assert response.status_code == 422

class TestNotFoundErrors:
    def test_update_nonexistent_task(self, client: TestClient):
        response = client.patch(
            "/tasks/99999",
            json={"title": "New title"}
        )
        
        assert response.status_code == 404
        assert response.json()["details"] == "Task not found"
    
    def test_archive_nonexistent_task(self, client: TestClient):
        response = client.post("/tasks/99999/archive")
        
        assert response.status_code == 404
        assert response.json()["details"] == "Task not found"
    
    def test_get_history_nonexistent_task(self, client: TestClient):
        response = client.get("/tasks/99999/history")
        
        assert response.status_code == 404
        assert response.json()["details"] == "Task not found"

class TestConflictErrors:
    def test_update_completed_task(self, client: TestClient, sample_completed_task):
        response = client.patch(
            f"/tasks/{sample_completed_task.id}",
            json={"title": "Update completed"}
        )
        
        assert response.status_code == 409
        assert response.json()["details"] == "Task has been already completed"

class TestSideEffects:
    def test_create_task_with_nonexistent_user_no_side_effect(self, client: TestClient, db_session):
        from app.database.models import Task
        
        initial_count = db_session.query(Task).count()
        
        response = client.post(
            "/tasks",
            params={"owner_id": 99999},
            json={
                "title": "Shouldn`t be created",
                "description": "User does not exist"
            }
        )
        
        assert response.status_code == 404
        
        final_count = db_session.query(Task).count()
        assert final_count == initial_count
    
    def test_update_nonexistent_task_no_side_effect(self, client: TestClient, sample_task, db_session):
        original_title = sample_task.title
        
        response = client.patch(
            "/tasks/99999",
            json={"title": "This should fail"}
        )
        
        assert response.status_code == 404
        
        from app.database.models import Task
        task = db_session.query(Task).filter(Task.id == sample_task.id).first()
        assert task.title == original_title
    
    def test_complete_already_completed_task_no_effect(self, client: TestClient, sample_completed_task, db_session):
        original_updated_at = sample_completed_task.updated_at
        
        response = client.post(f"/tasks/{sample_completed_task.id}/complete")
        
        assert response.status_code == 409
        
        from app.database.models import Task
        task = db_session.query(Task).filter(Task.id == sample_completed_task.id).first()
        assert task.status == "completed"
        assert task.updated_at == original_updated_at
    
    def test_assign_task_with_nonexistent_user_no_side_effect(self, client: TestClient, sample_task, db_session):
        original_assignee_id = sample_task.assignee_id
        
        response = client.post(
            f"/tasks/{sample_task.id}/assign",
            params={"user_id": 99999}
        )
        
        assert response.status_code == 404
        
        from app.database.models import Task
        task = db_session.query(Task).filter(Task.id == sample_task.id).first()
        assert task.assignee_id == original_assignee_id