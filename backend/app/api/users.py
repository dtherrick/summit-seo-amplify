"""User API routes."""
import logging
import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ..models.user import User, UserCreate, UserBase
from ..db.dynamodb import create_user, get_user
from ..utils.security import get_current_user, get_current_admin

logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

@router.get("/me", response_model=User)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    """Get the current user."""
    return current_user

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