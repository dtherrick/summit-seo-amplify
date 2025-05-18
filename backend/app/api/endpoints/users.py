from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any
from pydantic import BaseModel

from ...models.user import User, UserUpdate
from ...db.dynamodb import get_user_by_cognito_id, create_user, update_user
from ...utils.security import get_current_user

router = APIRouter()

@router.get("/me", response_model=User)
async def read_users_me(current_user: dict = Depends(get_current_user)) -> Any:
    """
    Get current user profile from DynamoDB.
    """
    user_data_from_db = await get_user_by_cognito_id(current_user["cognito_id"])
    if not user_data_from_db:
        raise HTTPException(status_code=404, detail="User not found")

    # Transform to match the User model
    transformed_user_data = user_data_from_db.copy()
    if 'user_id' in transformed_user_data:
        transformed_user_data['id'] = transformed_user_data.pop('user_id')

    # Ensure tenant_id is present or handle its absence.
    # For now, if it's missing, validation will still fail as the model requires it.
    # This needs to be investigated based on how tenant_id is populated.
    # Consider logging a warning if tenant_id is missing, as shown in thought process.

    return transformed_user_data

@router.put("/me", response_model=User)
async def update_users_me(
    user_in: UserUpdate,
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Update current user profile in DynamoDB.
    """
    user = await get_user_by_cognito_id(current_user["cognito_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Update fields
    update_data = user_in.model_dump(exclude_unset=True)
    if not update_data:
        return user  # No changes
    updated_user = await update_user(user["id"], update_data)
    return updated_user