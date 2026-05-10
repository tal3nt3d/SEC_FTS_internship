from tests import *

pytestmark = pytest.mark.api

class TestPatchMissingFields:
    def test_patch_update_only_title_other_fields_unchanged(self, client: TestClient, sample_task):
        original_title = sample_task.title
        original_description = sample_task.description
        original_status = sample_task.status
        
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={"title": "Updated Title"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["title"] == "Updated Title"
        assert data["title"] != original_title
        
        assert data["description"] == original_description
        assert data["status"] == original_status
    
    def test_patch_update_only_description_other_fields_unchanged(self, client: TestClient, sample_task):
        original_title = sample_task.title
        original_description = sample_task.description
        
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={"description": "Partially Updated Description"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["description"] == "Partially Updated Description"
        assert data["description"] != original_description
        assert data["title"] == original_title
    
    def test_patch_update_only_status_other_fields_unchanged(self, client: TestClient, sample_task):
        original_title = sample_task.title
        original_description = sample_task.description
        original_status = sample_task.status
        
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={"status": "in_progress"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "in_progress"
        assert data["status"] != original_status
        assert data["title"] == original_title
        assert data["description"] == original_description
    
    def test_patch_empty_json_no_changes(self, client: TestClient, sample_task):
        original_title = sample_task.title
        original_description = sample_task.description
        original_status = sample_task.status
        original_updated_at = sample_task.updated_at
        
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["title"] == original_title
        assert data["description"] == original_description
        assert data["status"] == original_status
        
class TestPatchNullValues:
    def test_patch_title_null_is_forbidden(self, client: TestClient, sample_task):
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={"title": None}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == sample_task.title
    
    def test_patch_description_null_is_forbidden(self, client: TestClient, sample_task):
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={"description": None}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == sample_task.description
    
    def test_patch_status_null_is_valid(self, client: TestClient, sample_task):
        original_status = sample_task.status
        
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={"status": None}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == original_status

class TestPatchForbiddenFields:
    def test_patch_cannot_change_id(self, client: TestClient, sample_task):
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={"id": 99999}
        )
        
        assert response.status_code == 422
        error_data = response.json()
        assert "details" in error_data
        assert "extra" in str(error_data["details"]).lower()
    
    def test_patch_cannot_change_owner_id(self, client: TestClient, sample_task):
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={"owner_id": 12345}
        )
        
        assert response.status_code == 422
        error_data = response.json()
        assert "extra" in str(error_data["details"]).lower()
    
    def test_patch_cannot_change_assignee_id_directly(self, client: TestClient, sample_task):
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={"assignee_id": 5}
        )
        
        assert response.status_code == 422
        error_data = response.json()
        assert "extra" in str(error_data["details"]).lower()
    
    def test_patch_cannot_change_created_at(self, client: TestClient, sample_task):
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={"created_at": "2024-01-01T00:00:00"}
        )
        
        assert response.status_code == 422
        error_data = response.json()
        assert "extra" in str(error_data["details"]).lower()
    
    def test_patch_cannot_change_closed_at(self, client: TestClient, sample_task):
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={"closed_at": "2024-12-31T23:59:59"}
        )
        
        assert response.status_code == 422
        error_data = response.json()
        assert "extra" in str(error_data["details"]).lower()
    
    def test_patch_extra_field_forbidden_by_schema(self, client: TestClient, sample_task):
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={"random_field": "some value"}
        )
        
        assert response.status_code == 422
        error_data = response.json()
        assert "extra" in str(error_data["details"]).lower()

class TestPatchPartialUpdateEdgeCases:
    def test_patch_update_multiple_fields_partially(self, client: TestClient, sample_task):
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={
                "title": "New Title",
                "status": "in_progress"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["title"] == "New Title"
        assert data["status"] == "in_progress"
        
        assert data["description"] == sample_task.description
    
    def test_patch_update_with_empty_string_title(self, client: TestClient, sample_task):
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={"title": ""}
        )
        
        assert response.status_code == 422
        error_data = response.json()
        assert "character" in str(error_data["details"])
    
    def test_patch_update_with_whitespace_only_title(self, client: TestClient, sample_task):
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={"title": "   "}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "   "
    
    def test_patch_update_title_to_max_length(self, client: TestClient, sample_task):
        max_title = "A" * 20
        
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={"title": max_title}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == max_title
        assert len(data["title"]) == 20
    
    def test_patch_update_title_exceeds_max_length(self, client: TestClient, sample_task):
        too_long_title = "A" * 21
        
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={"title": too_long_title}
        )
        
        assert response.status_code == 422
        error_data = response.json()
        assert "characters" in str(error_data["details"])
    
    def test_patch_update_description_to_max_length(self, client: TestClient, sample_task):
        max_description = "B" * 200
        
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={"description": max_description}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == max_description
        assert len(data["description"]) == 200
    
    def test_patch_update_description_exceeds_max_length(self, client: TestClient, sample_task):
        too_long_description = "B" * 201
        
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={"description": too_long_description}
        )
        
        assert response.status_code == 422


class TestPatchStatusTransitions:
    def test_patch_status_from_pending_to_in_progress(self, client: TestClient, sample_task):
        assert sample_task.status == "pending"
        
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={"status": "in_progress"}
        )
        
        assert response.status_code == 200
        assert response.json()["status"] == "in_progress"
    
    def test_patch_status_from_pending_to_completed(self, client: TestClient, sample_task):
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={"status": "completed"}
        )
        
        assert response.status_code == 200
        assert response.json()["status"] == "completed"
    
    def test_patch_status_from_completed_to_pending_forbidden(self, client: TestClient, sample_completed_task):
        response = client.patch(
            f"/tasks/{sample_completed_task.id}",
            json={"status": "pending"}
        )
        
        assert response.status_code == 409
        error_data = response.json()
        assert "already completed" in error_data["details"].lower()
    
    def test_patch_status_from_archived_forbidden(self, client: TestClient, sample_archived_task):
        response = client.patch(
            f"/tasks/{sample_archived_task.id}",
            json={"status": "pending"}
        )
        
        assert response.status_code == 200
        assert response.json()["status"] == "pending"

class TestPatchResponseContract:
    def test_patch_returns_full_task_object(self, client: TestClient, sample_task):
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={"title": "Updated Title"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        expected_fields = ["id", "title", "description", "status", "owner_id", 
                          "assignee_id", "created_at", "updated_at", "closed_at"]
        for field in expected_fields:
            assert field in data
    
    def test_patch_returns_updated_timestamp(self, client: TestClient, sample_task):
        original_updated_at = sample_task.updated_at
        
        import time
        time.sleep(1)
        
        response = client.patch(
            f"/tasks/{sample_task.id}",
            json={"title": "Timestamp update"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        new_updated_at = data["updated_at"]
        assert new_updated_at != original_updated_at