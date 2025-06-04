import pytest
from fastapi.testclient import TestClient
from fastapi import status, Depends
from unittest.mock import AsyncMock, patch, MagicMock
from botocore.exceptions import ClientError

from backend.app.main import app
from backend.app.models.user import User, UserUpdate
from backend.app.api.endpoints import users as users_endpoint

client = TestClient(app)

MOCK_USER = {
    "user_id": "user-123",
    "cognito_id": "cognito-abc",
    "email": "testuser@example.com",
    "full_name": "John Doe",
    "is_active": True,
    "tenant_id": "tenant-xyz",
    "subscription_tier": "free",
    "user_type": "user",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": None,
}

@pytest.fixture(autouse=True)
def patch_users_table():
    with patch("backend.app.db.dynamodb.users_table", new_callable=MagicMock) as mock_table:
        mock_table.query.return_value = {"Items": [MOCK_USER.copy()]}
        mock_table.get_item.return_value = {"Item": MOCK_USER.copy()}
        mock_table.update_item.return_value = {"Attributes": MOCK_USER.copy()}
        mock_table.put_item.return_value = {}
        yield mock_table

@pytest.fixture
def override_get_current_user():
    async def _override():
        return MOCK_USER
    app.dependency_overrides[users_endpoint.get_current_user] = _override
    yield
    app.dependency_overrides.pop(users_endpoint.get_current_user, None)

def test_read_users_me_success(patch_users_table, override_get_current_user):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == MOCK_USER["user_id"]
    assert data["email"] == MOCK_USER["email"]

def test_read_users_me_not_found(patch_users_table, override_get_current_user):
    patch_users_table.query.return_value = {"Items": []}
    response = client.get("/api/v1/users/me")
    assert response.status_code == 404

def test_update_users_me_partial_update(patch_users_table, override_get_current_user):
    patch_users_table.query.return_value = {"Items": [MOCK_USER.copy()]}
    updated_user_data = MOCK_USER.copy()
    updated_user_data["full_name"] = "Jane Doe"
    patch_users_table.update_item.return_value = {"Attributes": updated_user_data}
    response = client.put("/api/v1/users/me", json={"full_name": "Jane Doe"})
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Jane Doe"
    assert data["user_id"] == MOCK_USER["user_id"]

def test_update_users_me_noop(patch_users_table, override_get_current_user):
    patch_users_table.query.return_value = {"Items": [MOCK_USER.copy()]}
    response = client.put("/api/v1/users/me", json={})
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == MOCK_USER["user_id"]

def test_update_users_me_not_found(patch_users_table, override_get_current_user):
    patch_users_table.query.return_value = {"Items": []}
    response = client.put("/api/v1/users/me", json={"full_name": "Jane Doe"})
    assert response.status_code == 404

def test_update_users_me_dynamodb_error(patch_users_table, override_get_current_user):
    patch_users_table.query.return_value = {"Items": [MOCK_USER.copy()]}
    mock_error_response = {'Error': {'Code': 'InternalServerError', 'Message': 'DynamoDB broke'}}
    patch_users_table.update_item.side_effect = ClientError(mock_error_response, 'UpdateItem')
    response = client.put("/api/v1/users/me", json={"full_name": "Jane Doe"})
    assert response.status_code == 500