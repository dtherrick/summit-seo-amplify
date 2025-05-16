"""Business schemas module."""
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class BusinessBase(BaseModel):
    """Base schema for business data."""
    name: str
    customer_id: str
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)

class BusinessCreate(BusinessBase):
    """Schema for creating a new business."""
    pass

class BusinessUpdate(BaseModel):
    """Schema for updating a business."""
    name: Optional[str] = None
    customer_id: Optional[str] = None
    is_active: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)

class BusinessRead(BusinessBase):
    """Schema for reading business data."""
    id: UUID

class UserInBusiness(BaseModel):
    """Schema for user data in business context."""
    id: UUID
    email: str
    is_active: bool
    has_completed_survey: bool

    model_config = ConfigDict(from_attributes=True)

class BusinessWithUsers(BusinessRead):
    """Schema for business data with associated users."""
    users: List[UserInBusiness] 