"""Tests for the survey management API endpoints.

This module contains tests for survey response operations,
including creation, retrieval, and schema validation.

Test Coverage:
- Survey response creation
- Survey response retrieval
- Survey response listing
- Survey response updates
- Survey schema validation
- Error cases and edge conditions
"""

import pytest
from httpx import AsyncClient
from uuid import UUID

pytestmark = pytest.mark.asyncio

async def test_create_survey_response(
    client: AsyncClient,
    user_token: str,
    test_business: dict
):
    """Test creating a new survey response."""
    survey_data = {
        "customer_id": str(UUID(int=1)),
        "business_id": test_business["id"],
        "responses": {
            "satisfaction": 5,
            "recommendation_likelihood": 9,
            "feedback": "Great service!",
            "areas_for_improvement": ["None"]
        }
    }
    response = await client.post(
        "/api/v1/surveys",
        headers={"Authorization": f"Bearer {user_token}"},
        json=survey_data
    )
    assert response.status_code == 201
    created = response.json()
    assert created["customer_id"] == survey_data["customer_id"]
    assert created["business_id"] == str(test_business["id"])
    assert created["responses"] == survey_data["responses"]

async def test_get_survey_response(
    client: AsyncClient,
    user_token: str,
    test_business: dict
):
    """Test retrieving a specific survey response."""
    customer_id = str(UUID(int=1))
    response = await client.get(
        f"/api/v1/surveys/{customer_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    survey = response.json()
    assert survey["customer_id"] == customer_id
    assert survey["business_id"] == str(test_business["id"])
    assert "responses" in survey

async def test_list_survey_responses(
    client: AsyncClient,
    superuser_token: str
):
    """Test listing all survey responses with pagination."""
    response = await client.get(
        "/api/v1/surveys",
        headers={"Authorization": f"Bearer {superuser_token}"},
        params={"skip": 0, "limit": 10}
    )
    assert response.status_code == 200
    surveys = response.json()
    assert isinstance(surveys, list)
    assert len(surveys) <= 10  # Respects limit parameter

async def test_update_survey_response(
    client: AsyncClient,
    user_token: str,
    test_business: dict
):
    """Test updating an existing survey response."""
    customer_id = str(UUID(int=1))
    update_data = {
        "responses": {
            "satisfaction": 4,
            "recommendation_likelihood": 8,
            "feedback": "Updated feedback",
            "areas_for_improvement": ["Communication"]
        }
    }
    response = await client.put(
        f"/api/v1/surveys/{customer_id}",
        headers={"Authorization": f"Bearer {user_token}"},
        json=update_data
    )
    assert response.status_code == 200
    updated = response.json()
    assert updated["responses"] == update_data["responses"]

async def test_get_survey_schema(client: AsyncClient):
    """Test retrieving the survey schema definition."""
    response = await client.get("/api/v1/surveys/schema/structure")
    assert response.status_code == 200
    schema = response.json()
    assert "properties" in schema
    assert "responses" in schema["properties"]

async def test_get_survey_example(client: AsyncClient):
    """Test retrieving an example survey response."""
    response = await client.get("/api/v1/surveys/schema/example")
    assert response.status_code == 200
    example = response.json()
    assert "customer_id" in example
    assert "business_id" in example
    assert "responses" in example

async def test_create_survey_invalid_data(
    client: AsyncClient,
    user_token: str,
    test_business: dict
):
    """Test validation of survey response data."""
    invalid_data = {
        "customer_id": str(UUID(int=1)),
        "business_id": test_business["id"],
        "responses": {
            "satisfaction": 11,  # Invalid value (should be 1-5)
            "recommendation_likelihood": -1  # Invalid value (should be 0-10)
        }
    }
    response = await client.post(
        "/api/v1/surveys",
        headers={"Authorization": f"Bearer {user_token}"},
        json=invalid_data
    )
    assert response.status_code == 422  # Validation error

async def test_get_nonexistent_survey(
    client: AsyncClient,
    user_token: str
):
    """Test handling of requests for non-existent surveys."""
    nonexistent_id = str(UUID(int=999))
    response = await client.get(
        f"/api/v1/surveys/{nonexistent_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

async def test_unauthorized_survey_access(
    client: AsyncClient,
    user_token: str
):
    """Test accessing survey from different business."""
    other_customer_id = str(UUID(int=2))
    response = await client.get(
        f"/api/v1/surveys/{other_customer_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 404  # Not found for unauthorized access

async def test_create_duplicate_survey(
    client: AsyncClient,
    user_token: str,
    test_business: dict
):
    """Test creating duplicate survey for same customer."""
    survey_data = {
        "customer_id": str(UUID(int=1)),  # Already exists
        "business_id": test_business["id"],
        "responses": {
            "satisfaction": 5,
            "recommendation_likelihood": 9,
            "feedback": "Duplicate survey",
            "areas_for_improvement": ["None"]
        }
    }
    response = await client.post(
        "/api/v1/surveys",
        headers={"Authorization": f"Bearer {user_token}"},
        json=survey_data
    )
    assert response.status_code == 409  # Conflict

async def test_list_surveys_pagination(
    client: AsyncClient,
    superuser_token: str
):
    """Test survey listing pagination parameters."""
    # First page
    response1 = await client.get(
        "/api/v1/surveys",
        headers={"Authorization": f"Bearer {superuser_token}"},
        params={"skip": 0, "limit": 5}
    )
    assert response1.status_code == 200
    surveys1 = response1.json()
    
    # Second page
    response2 = await client.get(
        "/api/v1/surveys",
        headers={"Authorization": f"Bearer {superuser_token}"},
        params={"skip": 5, "limit": 5}
    )
    assert response2.status_code == 200
    surveys2 = response2.json()
    
    # Verify different results
    if len(surveys1) == 5 and len(surveys2) > 0:
        assert surveys1[0]["customer_id"] != surveys2[0]["customer_id"] 