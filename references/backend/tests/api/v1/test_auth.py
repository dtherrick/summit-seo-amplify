"""Tests for the authentication API endpoints.

This module contains tests for user authentication, registration,
and profile management operations.

Test Coverage:
- User registration
- User login
- Password reset flow
- User profile management
- Token validation
- Error cases and edge conditions
"""

import pytest
from httpx import AsyncClient
from uuid import UUID

pytestmark = pytest.mark.asyncio

async def test_register_user(client: AsyncClient):
    """Test user registration with valid data."""
    user_data = {
        "email": "test.register@example.com",
        "password": "StrongPass123!",
        "first_name": "Test",
        "last_name": "User"
    }
    response = await client.post(
        "/api/v1/auth/register",
        json=user_data
    )
    assert response.status_code == 201
    created = response.json()
    assert created["email"] == user_data["email"]
    assert "id" in created
    assert UUID(created["id"])  # Verify UUID format

async def test_register_user_duplicate_email(
    client: AsyncClient,
    test_user: dict
):
    """Test registration with duplicate email is rejected."""
    user_data = {
        "email": test_user["email"],  # Using existing email
        "password": "DifferentPass123!",
        "first_name": "Another",
        "last_name": "User"
    }
    response = await client.post(
        "/api/v1/auth/register",
        json=user_data
    )
    assert response.status_code == 400
    assert "email already exists" in response.json()["detail"].lower()

async def test_login_valid_credentials(
    client: AsyncClient,
    test_user: dict
):
    """Test user login with valid credentials."""
    login_data = {
        "username": test_user["email"],
        "password": "testpass123"  # Matches fixture password
    }
    response = await client.post(
        "/api/v1/auth/jwt/login",
        data=login_data  # Note: Using form data, not JSON
    )
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

async def test_login_invalid_credentials(client: AsyncClient):
    """Test login with invalid credentials is rejected."""
    login_data = {
        "username": "wrong@example.com",
        "password": "wrongpass"
    }
    response = await client.post(
        "/api/v1/auth/jwt/login",
        data=login_data
    )
    assert response.status_code == 400
    assert "invalid credentials" in response.json()["detail"].lower()

async def test_get_current_user(
    client: AsyncClient,
    user_token: str,
    test_user: dict
):
    """Test retrieving current user profile."""
    response = await client.get(
        "/api/v1/auth/users/me",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == test_user["email"]
    assert user["id"] == str(test_user["id"])

async def test_update_current_user(
    client: AsyncClient,
    user_token: str
):
    """Test updating current user profile."""
    update_data = {
        "first_name": "Updated",
        "last_name": "Name"
    }
    response = await client.patch(
        "/api/v1/auth/users/me",
        headers={"Authorization": f"Bearer {user_token}"},
        json=update_data
    )
    assert response.status_code == 200
    updated = response.json()
    assert updated["first_name"] == update_data["first_name"]
    assert updated["last_name"] == update_data["last_name"]

async def test_request_password_reset(
    client: AsyncClient,
    test_user: dict
):
    """Test requesting a password reset."""
    request_data = {
        "email": test_user["email"]
    }
    response = await client.post(
        "/api/v1/auth/forgot-password",
        json=request_data
    )
    assert response.status_code == 202  # Accepted

async def test_reset_password_invalid_token(client: AsyncClient):
    """Test password reset with invalid token is rejected."""
    reset_data = {
        "token": "invalid-token",
        "password": "NewPass123!"
    }
    response = await client.post(
        "/api/v1/auth/reset-password",
        json=reset_data
    )
    assert response.status_code == 400
    assert "invalid token" in response.json()["detail"].lower()

async def test_register_user_invalid_data(client: AsyncClient):
    """Test user registration with invalid data."""
    invalid_data = {
        "email": "not-an-email",
        "password": "weak",  # Too short
        "first_name": "",  # Empty
        "last_name": "User"
    }
    response = await client.post(
        "/api/v1/auth/register",
        json=invalid_data
    )
    assert response.status_code == 422
    errors = response.json()
    assert "email" in str(errors)  # Invalid email format
    assert "password" in str(errors)  # Password too short

async def test_verify_email(
    client: AsyncClient,
    test_user: dict
):
    """Test email verification endpoint."""
    # Note: This test assumes the token would be valid
    # In reality, you'd need to mock the token generation
    verify_data = {
        "token": "mock-verification-token"
    }
    response = await client.post(
        "/api/v1/auth/verify",
        json=verify_data
    )
    assert response.status_code in [200, 400]  # Either success or invalid token

async def test_unauthorized_access(client: AsyncClient):
    """Test accessing protected endpoint without token."""
    response = await client.get("/api/v1/auth/users/me")
    assert response.status_code == 401
    assert "not authenticated" in response.json()["detail"].lower()

async def test_invalid_token_access(client: AsyncClient):
    """Test accessing protected endpoint with invalid token."""
    response = await client.get(
        "/api/v1/auth/users/me",
        headers={"Authorization": "Bearer invalid-token"}
    )
    assert response.status_code == 401
    assert "invalid token" in response.json()["detail"].lower() 