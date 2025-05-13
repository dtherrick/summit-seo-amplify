"""User API routes."""
import logging
import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from botocore.exceptions import ClientError

from ..models.user import User, UserCreate, UserBase, UserUpdate
from ..db.dynamodb import create_user, get_user, update_user
from ..utils.security import get_current_user, get_current_admin

logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

@router.get("/me", response_model=User)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    """Get the current user."""
    return current_user

@router.put("/me", response_model=User)
async def update_user_me(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update the current user's profile."""
    user_id = current_user.get("id")
    if not user_id:
        # This should technically not happen if get_current_user works correctly
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials or find user ID")

    # Prepare update data, only including fields explicitly set in the request
    update_data = user_update.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No update data provided")

    # Add updated_at timestamp
    update_data["updated_at"] = datetime.utcnow().isoformat()

    try:
        updated_user_attributes = await update_user(user_id, update_data)
        if updated_user_attributes is None:
             # This case might occur if the user was deleted between get_current_user and update_user
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found during update")
        # Merge updated attributes with the potentially stale current_user dict for response model compliance
        # A fresh get_user call might be more robust but less performant
        response_user = {**current_user, **updated_user_attributes}
        return response_user
    except ClientError as e: # Already handled globally, but re-raising specific HTTP exceptions if needed
        logger.error(f"Failed to update user {user_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not update user profile")
    except Exception as e: # Catch any other unexpected errors
        logger.error(f"Unexpected error updating user {user_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

@router.get("/{user_id}", response_model=User)
async def read_user(
    user_id: str,
    current_user: dict = Depends(get_current_admin)
):
    """Get a user by ID (admin only)."""
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=User)
async def create_new_user(
    user: UserCreate,
    current_user: dict = Depends(get_current_admin)
):
    """Create a new user (admin only)."""
    # Generate a unique ID
    user_id = str(uuid.uuid4())

    # Create user object for database
    now = datetime.utcnow().isoformat()
    user_data = {
        "id": user_id,
        "tenant_id": user.tenant_id,
        "cognito_id": user.cognito_id,
        "email": user.email,
        "full_name": user.full_name,
        "is_active": user.is_active,
        "created_at": now,
        "updated_at": now,
        "user_type": "user",
        "subscription_tier": "free"
    }

    # Create the user in the database
    await create_user(user_data)

    return user_data