from tests import *

pytestmark = pytest.mark.export

class TestExportTasks:
    def test_export_tasks_returns_csv(self, client: TestClient, multiple_tasks):
        response = client.get("/tasks/export")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/vnd.ms-excel"
        assert "Content-Disposition" in response.headers
        assert "attachment; filename=tasks_export.csv" in response.headers["Content-Disposition"]
    
    def test_export_tasks_csv_structure(self, client: TestClient, multiple_tasks):
        response = client.get("/tasks/export")
        
        content = response.text
        
        assert content.startswith("\ufeff")
        
        csv_content = content[1:]
        
        reader = csv.reader(StringIO(csv_content))
        rows = list(reader)
        
        headers = rows[0]
        expected_headers = ["id", "title", "description", "status", "created_at", 
                           "updated_at", "closed_at", "owner_id", "assignee_id"]
        assert headers == expected_headers
        
        assert len(rows) == len(multiple_tasks) + 1
    
    def test_export_tasks_csv_data_consistency(self, client: TestClient, multiple_tasks):
        api_response = client.get("/tasks")
        api_tasks = api_response.json()
        
        export_response = client.get("/tasks/export")
        csv_content = export_response.text[1:]
        reader = csv.reader(StringIO(csv_content))
        rows = list(reader)
        headers = rows[0]
        csv_tasks = rows[1:]
        
        assert len(csv_tasks) == len(api_tasks)
        
        csv_by_id = {}
        for row in csv_tasks:
            task_id = int(row[0])
            csv_by_id[task_id] = {
                "title": row[1],
                "description": row[2],
                "status": row[3]
            }
        
        for api_task in api_tasks:
            csv_task = csv_by_id[api_task["id"]]
            assert csv_task["title"] == api_task["title"]
            assert csv_task["description"] == api_task["description"]
            assert csv_task["status"] == api_task["status"]
    
    def test_export_tasks_empty_database(self, client: TestClient):
        response = client.get("/tasks/export")
        
        csv_content = response.text[1:]
        reader = csv.reader(StringIO(csv_content))
        rows = list(reader)
    
        assert len(rows) == 1
        assert rows[0][0] == "id"
    
    def test_export_tasks_assignee_field_format(self, client: TestClient, sample_task, sample_assignee):
        client.post(f"/tasks/{sample_task.id}/assign", params={"user_id": sample_assignee.id})
        
        response = client.get("/tasks/export")
        csv_content = response.text[1:]
        reader = csv.reader(StringIO(csv_content))
        rows = list(reader)
        
        task_row = None
        for row in rows[1:]:
            if int(row[0]) == sample_task.id:
                task_row = row
                break
        
        assert task_row is not None
        assert task_row[8] == str(sample_assignee.id)
    
    def test_export_tasks_closed_at_format(self, client: TestClient, sample_task):
        client.post(f"/tasks/{sample_task.id}/complete")
        
        response = client.get("/tasks/export")
        csv_content = response.text[1:]
        reader = csv.reader(StringIO(csv_content))
        rows = list(reader)
        
        task_row = None
        for row in rows[1:]:
            if int(row[0]) == sample_task.id:
                task_row = row
                break
        
        assert task_row is not None
        assert task_row[6] != "" 