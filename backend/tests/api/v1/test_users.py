import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_update_user_me_validation_invalid_type(
    client, mock_dynamodb, mock_get_current_user
):
    """Test validation error for PUT /me with invalid data type."""
    response = await client.put(
        "/api/users/me",
        json={"full_name": 12345}  # Send integer instead of string
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "full_name" in response.text # Check that the error message mentions the field
    # Check that dynamodb update_item was NOT called
    mock_dynamodb.update_item.assert_not_called()

@pytest.mark.asyncio
async def test_update_user_me_validation_empty_payload(
    client, mock_dynamodb, mock_get_current_user
):
    """Test validation error for PUT /me with an empty JSON payload."""
    response = await client.put(
        "/api/users/me",
        json={} # Send empty payload
    )
    # The endpoint specifically checks for empty update_data after pydantic validation
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "No update data provided" in response.text
    # Check that dynamodb update_item was NOT called
    mock_dynamodb.update_item.assert_not_called()

@pytest.mark.asyncio
async def test_update_user_me_validation_extra_field(
    client, mock_dynamodb, mock_get_current_user, test_user_data
):
    """Test PUT /me ignores extra fields not in UserUpdate model."""
    update_payload = {
        "full_name": "Updated Name With Extra",
        "extra_field": "should_be_ignored"
    }
    # Mock the successful update in DynamoDB
    mock_dynamodb.update_item.return_value = {
        'Attributes': {**test_user_data, **{"full_name": "Updated Name With Extra", "updated_at": "some_iso_timestamp"}}
    }

    response = await client.put(
        "/api/users/me",
        json=update_payload
    )
    assert response.status_code == status.HTTP_200_OK
    # Verify the update_item call only contained the allowed fields (+ updated_at)
    mock_dynamodb.update_item.assert_called_once()
    call_args, call_kwargs = mock_dynamodb.update_item.call_args
    update_expr = call_kwargs.get("UpdateExpression")
    expr_attr_values = call_kwargs.get("ExpressionAttributeValues")

    assert "full_name" in update_expr
    assert ":full_name" in expr_attr_values
    assert expr_attr_values[":full_name"] == "Updated Name With Extra"
    assert "extra_field" not in update_expr # Ensure the extra field wasn't included
    assert ":extra_field" not in expr_attr_values
    assert "updated_at" in update_expr # Ensure updated_at was added

    # Check response body includes the update and ignores the extra field
    response_data = response.json()
    assert response_data["full_name"] == "Updated Name With Extra"
    assert "extra_field" not in response_data

# ... (Keep existing tests for admin endpoints if they exist)