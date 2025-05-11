from fastapi.testclient import TestClient
from typing import Dict

from backend.app.main import app  # Assuming your FastAPI app instance is here
from backend.app.api.endpoints.users import UserResponse, UserUpdate # Import your Pydantic models

client = TestClient(app)

# Mock data that aligns with your get_current_user_mock and endpoint responses
MOCK_COGNITO_SUB = "abcdef12-3456-7890-abcd-ef1234567890"
MOCK_EMAIL = "testuser@example.com"

DEFAULT_USER_PROFILE = {
    "user_id": MOCK_COGNITO_SUB,
    "email": MOCK_EMAIL,
    "first_name": "John",
    "last_name": "Doe",
    "is_active": True,
    "tenant_id": "mock-tenant-id",
    "subscription_tier": "free",
    "business_name": "MockBiz",
    "business_website": "https://mock.biz",
    "business_industry": "Tech",
    "user_type": "user"
}

# Helper to get auth headers for a mock user
# In a real scenario with actual auth, you might mock the dependency directly
# or use a fixture that provides a valid token for a test user.
# For now, since get_current_user_mock doesn't actually check a token,
# we don't strictly need to pass auth headers for these mock tests to pass,
# but it's good practice to think about it for when auth is real.

def get_mock_auth_headers() -> Dict[str, str]:
    return {"Authorization": "Bearer mocktoken"}


# Test for GET /api/v1/users/me
def test_read_users_me():
    response = client.get("/api/v1/users/me", headers=get_mock_auth_headers())
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == MOCK_COGNITO_SUB
    assert data["email"] == MOCK_EMAIL
    # Validate against the full expected mock profile
    for key, value in DEFAULT_USER_PROFILE.items():
        assert data[key] == value
    # Ensure it matches the UserResponse model structure (optional deep validation here)
    UserResponse(**data) # This will raise an error if the structure is wrong

# Tests for PUT /api/v1/users/me
def test_update_users_me_full_update():
    update_data = {
        "first_name": "Jane",
        "last_name": "Doer",
        "business_name": "UpdatedBiz",
        "business_website": "https://updated.biz",
        "business_industry": "E-commerce"
    }
    response = client.put("/api/v1/users/me", json=update_data, headers=get_mock_auth_headers())
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == update_data["first_name"]
    assert data["last_name"] == update_data["last_name"]
    assert data["business_name"] == update_data["business_name"]
    assert data["business_website"] == update_data["business_website"]
    assert data["business_industry"] == update_data["business_industry"]
    # Check that other fields remain as per the mock logic in the endpoint
    assert data["user_id"] == MOCK_COGNITO_SUB
    assert data["email"] == MOCK_EMAIL
    UserResponse(**data)

def test_update_users_me_partial_update():
    update_data = {
        "first_name": "Janey"
    }
    response = client.put("/api/v1/users/me", json=update_data, headers=get_mock_auth_headers())
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == update_data["first_name"]
    # Check that other fields remain as per the mock logic
    assert data["last_name"] == DEFAULT_USER_PROFILE["last_name"] # From original mock
    assert data["business_name"] == DEFAULT_USER_PROFILE["business_name"]
    UserResponse(**data)

def test_update_users_me_empty_payload():
    update_data = {}
    response = client.put("/api/v1/users/me", json=update_data, headers=get_mock_auth_headers())
    assert response.status_code == 200
    data = response.json()
    # Check that all fields remain as per the mock logic (original default values)
    for key, value in DEFAULT_USER_PROFILE.items():
        assert data[key] == value
    UserResponse(**data)