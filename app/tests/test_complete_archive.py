from tests import *

pytestmark = pytest.mark.api

class TestCompleteTask:
    def test_complete_pending_task_success(self, client: TestClient, sample_task):
        assert sample_task.status == "pending"
        assert sample_task.closed_at is None
        
        response = client.post(f"/tasks/{sample_task.id}/complete")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "completed"
        assert data["closed_at"] is not None
        
        closed_at = datetime.fromisoformat(data["closed_at"])
        assert closed_at <= datetime.now()
    
    def test_complete_nonexistent_task(self, client: TestClient):
        response = client.post("/tasks/99999/complete")
        
        assert response.status_code == 404
        assert response.json()["details"] == "Task not found"
    
    def test_complete_already_archived_task(self, client: TestClient, sample_task, db_session):
        from app.service.tasks import TaskService
        from app.dependencies.tasks import get_task_service
        
        service = TaskService(db_session)
        service.archive_task(sample_task.id)
        
        response = client.post(f"/tasks/{sample_task.id}/complete")
        
        assert response.status_code == 200
        
    def test_complete_already_completed_task(self, client: TestClient, sample_completed_task):
        response = client.post(f"/tasks/{sample_completed_task.id}/complete")
        
        assert response.status_code == 409
        error_data = response.json()
        assert error_data["details"] == "Task has been already completed"
        
    def test_assign_nonexistent_task(self, client: TestClient, sample_user):
        response = client.post(
            "/tasks/99999/assign",
            params={"user_id": sample_user.id}
        )
        
        assert response.status_code == 404
        assert response.json()["details"] == "Task not found"
    
    def test_assign_task_to_nonexistent_user(self, client: TestClient, sample_task):
        response = client.post(
            f"/tasks/{sample_task.id}/assign",
            params={"user_id": 99999}
        )
        
        assert response.status_code == 404
        assert response.json()["details"] == "User not found"
        
    def test_assign_completed_task(self, client: TestClient, sample_completed_task, sample_assignee):
        response = client.post(
            f"/tasks/{sample_completed_task.id}/assign",
            params={"user_id": sample_assignee.id}
        )
        
        assert response.status_code == 409
        assert "completed" in response.json()["details"].lower()
        
    def test_archive_already_archived_task(self, client: TestClient, sample_task):
        client.post(f"/tasks/{sample_task.id}/archive")
        
        response = client.post(f"/tasks/{sample_task.id}/archive")
        
        assert response.status_code == 409
        assert response.json()["details"] == "Task has been already archived"
        
    def test_archive_completed_task(self, client: TestClient, sample_completed_task):
        response = client.post(f"/tasks/{sample_completed_task.id}/archive")
        
        assert response.status_code == 409