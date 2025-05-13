"""User model definitions."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr

class UserBase(BaseModel):
    """Base user model."""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True

class UserUpdate(BaseModel):
    """User update model for partial updates."""
    # email: Optional[EmailStr] = None # Disable email update for now
    full_name: Optional[str] = None
    # is_active: Optional[bool] = None # Disable active status update for now

class UserCreate(UserBase):
    """User creation model."""
    tenant_id: str
    cognito_id: str

class UserInDB(UserBase):
    """User model as stored in the database."""
    id: str
    tenant_id: str
    cognito_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    user_type: str = "user"  # Options: "user", "admin", "system"
    subscription_tier: str = "free"  # Options: "free", "basic", "premium"

class User(UserInDB):
    """API user model."""
    pass