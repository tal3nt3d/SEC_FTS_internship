from tests import *

pytestmark = pytest.mark.api

class TestCreateTask:
    def test_create_task_success(self, client: TestClient, sample_user):
        response = client.post(
            "/tasks",
            params={"owner_id": sample_user.id},
            json={
                "title": "Complete assignment",
                "description": "Finish the pytest configuration"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        
        task = TaskResponse(**data)
        
        assert task.id > 0
        assert task.title == "Complete assignment"
        assert task.description == "Finish the pytest configuration"
        assert task.status == "pending"
        assert task.owner_id == sample_user.id
        assert task.assignee_id is None
        assert task.created_at is not None
        assert task.updated_at is not None
        assert task.closed_at is None
    
    def test_create_task_with_nonexistent_user(self, client: TestClient):
        response = client.post(
            "/tasks",
            params={"owner_id": 99999},
            json={
                "title": "Test task",
                "description": "This user does not exist"
            }
        )
        
        assert response.status_code == 404
        assert response.json()["details"] == "User not found"
    
    def test_create_task_invalid_title_too_short(self, client: TestClient, sample_user):
        response = client.post(
            "/tasks",
            params={"owner_id": sample_user.id},
            json={
                "title": "",
                "description": "Valid description"
            }
        )
        
        assert response.status_code == 422
        errors = response.json()["details"]
        assert any("character" in str(error) for error in errors)
    
    def test_create_task_invalid_title_too_long(self, client: TestClient, sample_user):
        response = client.post(
            "/tasks",
            params={"owner_id": sample_user.id},
            json={
                "title": "A" * 21,
                "description": "Valid description"
            }
        )
        
        assert response.status_code == 422
        errors = response.json()["details"]
        assert any("characters" in str(error) for error in errors)
    
    def test_create_task_invalid_description_too_long(self, client: TestClient, sample_user):
        response = client.post(
            "/tasks",
            params={"owner_id": sample_user.id},
            json={
                "title": "Valid title",
                "description": "B" * 201
            }
        )
        
        assert response.status_code == 422
        errors = response.json()["details"]
        assert any("characters" in str(error) for error in errors)
    
    def test_create_task_extra_fields_forbidden(self, client: TestClient, sample_user):
        response = client.post(
            "/tasks",
            params={"owner_id": sample_user.id},
            json={
                "title": "Test task",
                "description": "Test description",
                "extra_field": "should be forbidden"
            }
        )
        
        assert response.status_code == 422


class TestGetTask:
    def test_get_task_success(self, client: TestClient, sample_task):
        response = client.get(f"/tasks/{sample_task.id}")
        
        assert response.status_code == 200
        data = response.json()
        
        task = TaskResponse(**data)
        
        assert task.id == sample_task.id
        assert task.title == sample_task.title
        assert task.description == sample_task.description
        assert task.status == sample_task.status
        assert task.owner_id == sample_task.owner_id
    
    def test_get_nonexistent_task(self, client: TestClient):
        response = client.get("/tasks/99999")
        
        assert response.status_code == 404
        assert response.json()["details"] == "Task not found"
    
    def test_get_task_negative_id(self, client: TestClient):
        response = client.get("/tasks/-1")
        
        assert response.status_code == 404
        assert response.json()["details"] == "Task not found"