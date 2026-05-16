from tests import *

pytestmark = pytest.mark.auth

class TestAuthentication:
    def test_access_without_auth(self, client: TestClient):
        response = client.get("/tasks")
        
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]
    
    def test_access_with_invalid_token(self, client: TestClient):
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/tasks", headers=headers)
        
        assert response.status_code == 401
        assert "stub" in response.json()["detail"]
    
    def test_access_with_valid_stub_token(self, client: TestClient, sample_user):
        headers = {"Authorization": f"Bearer stub_{sample_user.id}"}
        response = client.get("/tasks", headers=headers)
        
        assert response.status_code == 200
    
    def test_access_with_nonexistent_user(self, client: TestClient):
        headers = {"Authorization": "Bearer stub_99999"}
        response = client.get("/tasks", headers=headers)
        
        assert response.status_code == 404

class TestOwnerAccess:
    def test_owner_can_get_own_task(self, client: TestClient, sample_user, sample_task):
        headers = {"Authorization": f"Bearer stub_{sample_user.id}"}
        response = client.get(f"/tasks/{sample_task.id}", headers=headers)
        
        assert response.status_code == 200
        assert response.json()["id"] == sample_task.id
    
    def test_owner_can_update_own_task(self, client: TestClient, sample_user, sample_task):
        headers = {"Authorization": f"Bearer stub_{sample_user.id}"}
        update_data = {"title": "Updated Title"}
        response = client.patch(f"/tasks/{sample_task.id}", json=update_data, headers=headers)
        
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"
    
    def test_owner_can_complete_own_task(self, client: TestClient, sample_user, sample_task):
        headers = {"Authorization": f"Bearer stub_{sample_user.id}"}
        response = client.post(f"/tasks/{sample_task.id}/complete", headers=headers)
        
        assert response.status_code == 200
        assert response.json()["status"] == "completed"
        assert response.json()["closed_at"] is not None
    
    def test_owner_can_archive_own_task(self, client: TestClient, sample_user, sample_task):
        headers = {"Authorization": f"Bearer stub_{sample_user.id}"}
        response = client.post(f"/tasks/{sample_task.id}/archive", headers=headers)
        
        assert response.status_code == 200
        assert response.json()["status"] == "archived"
    
    def test_owner_can_assign_executor_to_own_task(self, client: TestClient, sample_user, sample_task, sample_assignee):
        headers = {"Authorization": f"Bearer stub_{sample_user.id}"}
        response = client.post(
            f"/tasks/{sample_task.id}/assign",
            params={"user_id": sample_assignee.id},
            headers=headers
        )
        
        assert response.status_code == 200
        assert response.json()["assignee_id"] == sample_assignee.id

class TestForeignUserDenied:
    def test_other_user_cannot_get_foreign_task(self, client: TestClient, other_user, sample_task):
        headers = {"Authorization": f"Bearer stub_{other_user.id}"}
        response = client.get(f"/tasks/{sample_task.id}", headers=headers)
        
        assert response.status_code == 403
    
    def test_other_user_cannot_update_foreign_task(self, client: TestClient, other_user, sample_task):
        headers = {"Authorization": f"Bearer stub_{other_user.id}"}
        update_data = {"title": "Hacked Title"}
        response = client.patch(f"/tasks/{sample_task.id}", json=update_data, headers=headers)
        
        assert response.status_code == 403
    
    def test_other_user_cannot_complete_foreign_task(self, client: TestClient, other_user, sample_task):
        headers = {"Authorization": f"Bearer stub_{other_user.id}"}
        response = client.post(f"/tasks/{sample_task.id}/complete", headers=headers)
        
        assert response.status_code == 403
    
    def test_other_user_cannot_archive_foreign_task(self, client: TestClient, other_user, sample_task):
        headers = {"Authorization": f"Bearer stub_{other_user.id}"}
        response = client.post(f"/tasks/{sample_task.id}/archive", headers=headers)
        
        assert response.status_code == 403
    
    def test_other_user_cannot_assign_executor_to_foreign_task(self, client: TestClient, other_user, sample_task, sample_assignee):
        headers = {"Authorization": f"Bearer stub_{other_user.id}"}
        response = client.post(
            f"/tasks/{sample_task.id}/assign",
            params={"user_id": sample_assignee.id},
            headers=headers
        )
        
        assert response.status_code == 403

class TestAdminAccess:
    def test_admin_can_get_foreign_task(self, client: TestClient, admin_user, sample_task_other_owner):
        headers = {"Authorization": f"Bearer stub_{admin_user.id}"}
        response = client.get(f"/tasks/{sample_task_other_owner.id}", headers=headers)
        
        assert response.status_code == 200
        assert response.json()["id"] == sample_task_other_owner.id
    
    def test_admin_can_update_foreign_task(self, client: TestClient, admin_user, sample_task_other_owner):
        headers = {"Authorization": f"Bearer stub_{admin_user.id}"}
        update_data = {"title": "Admin Updated"}
        response = client.patch(f"/tasks/{sample_task_other_owner.id}", json=update_data, headers=headers)
        
        assert response.status_code == 200
        assert response.json()["title"] == "Admin Updated"
    
    def test_admin_can_complete_foreign_task(self, client: TestClient, admin_user, sample_task_other_owner):
        headers = {"Authorization": f"Bearer stub_{admin_user.id}"}
        response = client.post(f"/tasks/{sample_task_other_owner.id}/complete", headers=headers)
        
        assert response.status_code == 200
        assert response.json()["status"] == "completed"
    
    def test_admin_can_archive_foreign_task(self, client: TestClient, admin_user, sample_task_other_owner):
        headers = {"Authorization": f"Bearer stub_{admin_user.id}"}
        response = client.post(f"/tasks/{sample_task_other_owner.id}/archive", headers=headers)
        
        assert response.status_code == 200
        assert response.json()["status"] == "archived"
    
    def test_admin_can_assign_executor_to_foreign_task(self, client: TestClient, admin_user, sample_task_other_owner, sample_assignee):
        headers = {"Authorization": f"Bearer stub_{admin_user.id}"}
        response = client.post(
            f"/tasks/{sample_task_other_owner.id}/assign",
            params={"user_id": sample_assignee.id},
            headers=headers
        )
        
        assert response.status_code == 200
        assert response.json()["assignee_id"] == sample_assignee.id

class TestTaskListFiltering:
    def test_user_sees_only_own_tasks_in_list(self, client: TestClient, sample_user, sample_task_other_owner):
        headers = {"Authorization": f"Bearer stub_{sample_user.id}"}
        response = client.get("/tasks", headers=headers)
        
        assert response.status_code == 200
        tasks = response.json()
        
        for task in tasks:
            assert task["owner_id"] == sample_user.id
    
    def test_admin_sees_all_tasks_in_list(self, client, admin_user, sample_task_other_owner):
        headers = {"Authorization": f"Bearer stub_{admin_user.id}"}
        response = client.get("/tasks", headers=headers)
        
        assert response.status_code == 200
        tasks = response.json()
        
        owner_ids = {task["owner_id"] for task in tasks}
        assert len(owner_ids) >= 1 

class TestSummaryFiltering:
    def test_user_sees_only_own_tasks_in_summary(self, client: TestClient, sample_user, multiple_tasks):
        headers = {"Authorization": f"Bearer stub_{sample_user.id}"}
        response = client.get("/tasks/summary", headers=headers)
        
        assert response.status_code == 200
        summary = response.json()
        
        total_tasks = summary["total"]
        user_tasks_count = len([t for t in multiple_tasks if t["owner_id"] == sample_user.id])
        
        assert total_tasks == user_tasks_count
    
    def test_admin_sees_all_tasks_in_summary(self, client, admin_user, sample_task_other_owner):
        headers = {"Authorization": f"Bearer stub_{admin_user.id}"}
        response = client.get("/tasks/summary", headers=headers)
        
        assert response.status_code == 200
        summary = response.json()
        
        assert summary["total"] > 0