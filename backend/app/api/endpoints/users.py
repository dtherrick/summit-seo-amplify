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

    # The data from get_user_by_cognito_id should already conform to UserInDB (which has user_id)
    # No transformation needed if get_user_by_cognito_id returns the correct structure.
    # Remove erroneous transformation:
    # transformed_user_data = user_data_from_db.copy()
    # if 'user_id' in transformed_user_data:
    #     transformed_user_data['id'] = transformed_user_data.pop('user_id')

    return user_data_from_db

@router.put("/me", response_model=User)
async def update_users_me(
    user_in: UserUpdate,
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Update current user profile in DynamoDB.
    """
    user_data_from_db = await get_user_by_cognito_id(current_user["cognito_id"])
    if not user_data_from_db:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_in.model_dump(exclude_unset=True)

    if not update_data:
        return user_data_from_db  # No changes, return data that should match User model

    # Assuming user_data_from_db contains 'user_id' as the primary key
    updated_user = await update_user(user_data_from_db["user_id"], update_data)
    return updated_user