"""Tests for the business management API endpoints.

This module contains tests for the business CRUD operations,
focusing on authentication, authorization, and data validation.

Test Coverage:
- Business listing (with auth checks)
- Business creation
- Business retrieval
- Business updates
- Business deletion
- Error cases and edge conditions
"""

import pytest
from httpx import AsyncClient
from uuid import UUID

pytestmark = pytest.mark.asyncio

async def test_list_businesses_superuser(
    client: AsyncClient,
    superuser_token: str,
    test_business: dict
):
    """Test listing businesses as superuser."""
    response = await client.get(
        "/api/v1/businesses",
        headers={"Authorization": f"Bearer {superuser_token}"}
    )
    assert response.status_code == 200
    businesses = response.json()
    assert isinstance(businesses, list)
    assert len(businesses) > 0
    assert businesses[0]["name"] == test_business["name"]

async def test_list_businesses_regular_user(
    client: AsyncClient,
    user_token: str
):
    """Test that regular users cannot list all businesses."""
    response = await client.get(
        "/api/v1/businesses",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403

async def test_create_business_superuser(
    client: AsyncClient,
    superuser_token: str
):
    """Test creating a new business as superuser."""
    business_data = {
        "name": "New Test Business",
        "description": "Created in test",
        "is_active": True
    }
    response = await client.post(
        "/api/v1/businesses",
        headers={"Authorization": f"Bearer {superuser_token}"},
        json=business_data
    )
    assert response.status_code == 201
    created = response.json()
    assert created["name"] == business_data["name"]
    assert UUID(created["id"])  # Verify UUID format

async def test_create_business_regular_user(
    client: AsyncClient,
    user_token: str
):
    """Test that regular users cannot create businesses."""
    business_data = {
        "name": "Unauthorized Business",
        "description": "Should not be created",
        "is_active": True
    }
    response = await client.post(
        "/api/v1/businesses",
        headers={"Authorization": f"Bearer {user_token}"},
        json=business_data
    )
    assert response.status_code == 403

async def test_get_business_owner(
    client: AsyncClient,
    user_token: str,
    test_business: dict
):
    """Test retrieving own business details."""
    response = await client.get(
        f"/api/v1/businesses/{test_business['id']}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    business = response.json()
    assert business["id"] == str(test_business["id"])
    assert business["name"] == test_business["name"]

async def test_get_business_other(
    client: AsyncClient,
    user_token: str
):
    """Test that users cannot access other businesses."""
    other_id = "123e4567-e89b-12d3-a456-426614174000"
    response = await client.get(
        f"/api/v1/businesses/{other_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 404

async def test_update_business_superuser(
    client: AsyncClient,
    superuser_token: str,
    test_business: dict
):
    """Test updating a business as superuser."""
    update_data = {
        "name": "Updated Business Name",
        "description": "Updated in test"
    }
    response = await client.patch(
        f"/api/v1/businesses/{test_business['id']}",
        headers={"Authorization": f"Bearer {superuser_token}"},
        json=update_data
    )
    assert response.status_code == 200
    updated = response.json()
    assert updated["name"] == update_data["name"]
    assert updated["description"] == update_data["description"]

async def test_update_business_regular_user(
    client: AsyncClient,
    user_token: str,
    test_business: dict
):
    """Test that regular users cannot update businesses."""
    update_data = {
        "name": "Should Not Update",
        "description": "Should fail"
    }
    response = await client.patch(
        f"/api/v1/businesses/{test_business['id']}",
        headers={"Authorization": f"Bearer {user_token}"},
        json=update_data
    )
    assert response.status_code == 403

async def test_delete_business_superuser(
    client: AsyncClient,
    superuser_token: str,
    test_business: dict
):
    """Test deleting a business as superuser."""
    response = await client.delete(
        f"/api/v1/businesses/{test_business['id']}",
        headers={"Authorization": f"Bearer {superuser_token}"}
    )
    assert response.status_code == 204

    # Verify deletion
    response = await client.get(
        f"/api/v1/businesses/{test_business['id']}",
        headers={"Authorization": f"Bearer {superuser_token}"}
    )
    assert response.status_code == 404

async def test_delete_business_regular_user(
    client: AsyncClient,
    user_token: str,
    test_business: dict
):
    """Test that regular users cannot delete businesses."""
    response = await client.delete(
        f"/api/v1/businesses/{test_business['id']}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403

async def test_get_nonexistent_business(
    client: AsyncClient,
    superuser_token: str
):
    """Test handling of requests for non-existent businesses."""
    nonexistent_id = "123e4567-e89b-12d3-a456-426614174000"
    response = await client.get(
        f"/api/v1/businesses/{nonexistent_id}",
        headers={"Authorization": f"Bearer {superuser_token}"}
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

async def test_create_business_invalid_data(
    client: AsyncClient,
    superuser_token: str
):
    """Test validation of business creation data."""
    invalid_data = {
        # Missing required 'name' field
        "description": "Invalid business data",
        "is_active": True
    }
    response = await client.post(
        "/api/v1/businesses",
        headers={"Authorization": f"Bearer {superuser_token}"},
        json=invalid_data
    )
    assert response.status_code == 422  # Validation error 