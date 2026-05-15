from tests import *

pytestmark = pytest.mark.api

class TestGetTasksList:
    def test_get_tasks_empty_list(self, client: TestClient):
        response = client.get("/tasks")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_get_tasks_returns_all_tasks(self, client: TestClient, multiple_tasks):
        response = client.get("/tasks")
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data) == len(multiple_tasks)
        
        for task in data:
            task_valid = TaskResponse(**task)
            assert task_valid
    
    def test_get_tasks_filter_by_status(self, client: TestClient, multiple_tasks):
        response = client.get("/tasks?status=pending")
        
        assert response.status_code == 200
        data = response.json()
        
        for task in data:
            assert task["status"] == "pending"
        
        assert len(data) == 2
    
    def test_get_tasks_filter_by_user_id(self, client: TestClient, sample_user, multiple_tasks):
        response = client.get(f"/tasks?user_id={sample_user.id}")
        
        assert response.status_code == 200
        data = response.json()
        
        for task in data:
            assert task["owner_id"] == sample_user.id
        
        assert len(data) == len(multiple_tasks)
    
    def test_get_tasks_filter_by_nonexistent_user(self, client: TestClient):
        response = client.get("/tasks?user_id=99999")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_get_tasks_filter_by_status_and_user(self, client: TestClient, sample_user, multiple_tasks):
        response = client.get(f"/tasks?status=pending&user_id={sample_user.id}")
        
        assert response.status_code == 200
        data = response.json()
        
        for task in data:
            assert task["status"] == "pending"
            assert task["owner_id"] == sample_user.id
    
    def test_get_tasks_sort_by_created_at_asc(self, client: TestClient, multiple_tasks):
        response = client.get("/tasks?sort_by=created_at&order=asc")
        
        assert response.status_code == 200
        data = response.json()
        
        created_dates = [datetime.fromisoformat(task["created_at"]) for task in data]
        assert created_dates == sorted(created_dates)
    
    def test_get_tasks_sort_by_created_at_desc(self, client: TestClient, multiple_tasks):
        response = client.get("/tasks?sort_by=created_at&order=desc")
        
        assert response.status_code == 200
        data = response.json()
        
        created_dates = [datetime.fromisoformat(task["created_at"]) for task in data]
        assert created_dates == sorted(created_dates, reverse=True)
    
    def test_get_tasks_sort_by_updated_at(self, client: TestClient, multiple_tasks):
        response = client.get("/tasks?sort_by=updated_at&order=asc")
        
        assert response.status_code == 200
        data = response.json()
        
        updated_dates = [datetime.fromisoformat(task["updated_at"]) for task in data]
        assert updated_dates == sorted(updated_dates)
    
    def test_get_tasks_default_sorting(self, client: TestClient, multiple_tasks):
        response = client.get("/tasks")
        
        assert response.status_code == 200
        data = response.json()
        
        created_dates = [datetime.fromisoformat(task["created_at"]) for task in data]
        assert created_dates == sorted(created_dates, reverse=True)
    
    def test_get_tasks_pagination_limit(self, client: TestClient, multiple_tasks):
        response = client.get("/tasks?limit=2")
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data) == 2
    
    def test_get_tasks_pagination_offset(self, client: TestClient, multiple_tasks):
        response1 = client.get("/tasks?limit=?&offset=?", params={"limit": 2, "offset": 0})
        data1 = response1.json()
        
        response2 = client.get("/tasks?limit=?&offset=?", params={"limit": 2, "offset": 2})
        data2 = response2.json()
        
        assert len(data1) == 2
        assert len(data2) == 2
        assert data1[0]["id"] != data2[0]["id"]
        
        ids1 = {task["id"] for task in data1}
        ids2 = {task["id"] for task in data2}
        assert ids1.isdisjoint(ids2)
    
    def test_get_tasks_pagination_with_filter(self, client: TestClient, multiple_tasks):
        response = client.get("/tasks?status=?&limit=?&offset=?", params={"status": "pending", "limit": 1, "offset": 0})
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data) == 1
        assert data[0]["status"] == "pending"
    
    def test_get_tasks_invalid_limit_negative(self, client: TestClient):
        response = client.get("/tasks?limit=?", params={"limit": -5})
        
        assert response.status_code == 422
    
    def test_get_tasks_invalid_offset_negative(self, client: TestClient):
        response = client.get("/tasks?offset=?", params={"offset": -1})
        
        assert response.status_code == 422
    
    def test_get_tasks_invalid_sort_by(self, client: TestClient):
        response = client.get("/tasks?sort_by=?", params={"sort_by": "invalid_field"})
        
        assert response.status_code == 422
    
    def test_get_tasks_invalid_order(self, client: TestClient):
        response = client.get("/tasks?order=?", params={"order": "invalid_order"})
        
        assert response.status_code == 422
        
class TestGetTasksSummary:
    def test_get_summary_returns_correct_structure(self, client: TestClient, multiple_tasks):
        response = client.get("/tasks/summary")
        
        assert response.status_code == 200
        data = response.json()
        
        expected_fields = ["total", "pending", "in_progress", "completed", "archived"]
        for field in expected_fields:
            assert field in data
            assert isinstance(data[field], int)
            assert data[field] >= 0
    
    def test_get_summary_counts_match_actual_tasks(self, client: TestClient, multiple_tasks):
        response = client.get("/tasks/summary")
        
        assert response.status_code == 200
        data = response.json()
        
        summary = TasksSummary(**data)
        
        assert summary.total == 5
        assert summary.pending == 2
        assert summary.in_progress == 1
        assert summary.completed == 1
        assert summary.archived == 1
    
    def test_get_summary_empty_database(self, client: TestClient, db_session):
        response = client.get("/tasks/summary")
        
        assert response.status_code == 200
        data = response.json()
        
        summary = TasksSummary(**data)
        
        assert summary.total == 0
        assert summary.pending == 0
        assert summary.in_progress == 0
        assert summary.completed == 0
        assert summary.archived == 0
    
    def test_get_summary_after_task_completion(self, client: TestClient, sample_task):
        response1 = client.get("/tasks/summary")
        assert response1.json()["pending"] == 1
        assert response1.json()["completed"] == 0
        
        client.post(f"/tasks/{sample_task.id}/complete")
        
        response2 = client.get("/tasks/summary")
        assert response2.json()["pending"] == 0
        assert response2.json()["completed"] == 1