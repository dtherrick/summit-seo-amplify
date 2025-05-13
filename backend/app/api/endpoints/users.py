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
    user = await get_user_by_cognito_id(current_user["cognito_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

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