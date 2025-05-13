import pytest
from fastapi.testclient import TestClient
from fastapi import status, Depends
from unittest.mock import AsyncMock, patch, MagicMock

from backend.app.main import app
from backend.app.models.user import User, UserUpdate
from backend.app.api.endpoints import users as users_endpoint

client = TestClient(app)

MOCK_USER = {
    "id": "user-123",
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
    with patch("backend.app.db.dynamodb.users_table", MagicMock()) as mock_table:
        # For get_user_by_cognito_id (query)
        mock_table.query.return_value = {"Items": [MOCK_USER]}
        # For get_user (get_item)
        mock_table.get_item.return_value = {"Item": MOCK_USER}
        # For update_user (update_item)
        mock_table.update_item.return_value = {"Attributes": MOCK_USER}
        # For create_user (put_item)
        mock_table.put_item.return_value = {}
        yield mock_table

@pytest.fixture
def override_get_current_user():
    async def _override():
        return MOCK_USER
    app.dependency_overrides[users_endpoint.get_current_user] = _override
    yield
    app.dependency_overrides.pop(users_endpoint.get_current_user, None)

@patch("backend.app.db.dynamodb.get_user_by_cognito_id", new_callable=AsyncMock)
def test_read_users_me_success(mock_get_user, override_get_current_user):
    mock_get_user.return_value = MOCK_USER
    response = client.get("/api/v1/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == MOCK_USER["id"]
    assert data["email"] == MOCK_USER["email"]

@patch("backend.app.db.dynamodb.get_user_by_cognito_id", new_callable=AsyncMock)
def test_read_users_me_not_found(mock_get_user, override_get_current_user):
    mock_get_user.return_value = None
    response = client.get("/api/v1/users/me")
    assert response.status_code == 404

@patch("backend.app.db.dynamodb.get_user_by_cognito_id", new_callable=AsyncMock)
@patch("backend.app.db.dynamodb.update_user", new_callable=AsyncMock)
def test_update_users_me_partial_update(mock_update_user, mock_get_user, override_get_current_user):
    mock_get_user.return_value = MOCK_USER.copy()
    updated = MOCK_USER.copy()
    updated["full_name"] = "Jane Doe"
    mock_update_user.return_value = updated
    response = client.put("/api/v1/users/me", json={"full_name": "Jane Doe"})
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Jane Doe"
    assert data["id"] == MOCK_USER["id"]

@patch("backend.app.db.dynamodb.get_user_by_cognito_id", new_callable=AsyncMock)
@patch("backend.app.db.dynamodb.update_user", new_callable=AsyncMock)
def test_update_users_me_noop(mock_update_user, mock_get_user, override_get_current_user):
    mock_get_user.return_value = MOCK_USER.copy()
    response = client.put("/api/v1/users/me", json={})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == MOCK_USER["id"]
    mock_update_user.assert_not_called()

@patch("backend.app.db.dynamodb.get_user_by_cognito_id", new_callable=AsyncMock)
def test_update_users_me_not_found(mock_get_user, override_get_current_user):
    mock_get_user.return_value = None
    response = client.put("/api/v1/users/me", json={"full_name": "Jane Doe"})
    assert response.status_code == 404

@patch("backend.app.db.dynamodb.get_user_by_cognito_id", new_callable=AsyncMock)
@patch("backend.app.db.dynamodb.update_user", new_callable=AsyncMock)
def test_update_users_me_dynamodb_error(mock_update_user, mock_get_user, override_get_current_user):
    mock_get_user.return_value = MOCK_USER.copy()
    mock_update_user.side_effect = Exception("DynamoDB error")
    response = client.put("/api/v1/users/me", json={"full_name": "Jane Doe"})
    assert response.status_code == 500 or response.status_code == 422