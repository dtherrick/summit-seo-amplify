"""Authentication schemas module."""
from typing import List, Optional
from uuid import UUID

from fastapi_users import schemas
from pydantic import EmailStr, model_validator

class UserRead(schemas.BaseUser[UUID]):
    """Schema for reading user data."""
    business_id: Optional[UUID] = None
    has_completed_survey: bool
    roles: List[str] = []

    class Config:
        """Pydantic configuration."""
        from_attributes = True

class UserCreate(schemas.BaseUserCreate):
    """Schema for creating a new user."""
    business_id: Optional[UUID] = None
    has_completed_survey: bool = False
    roles: List[str] = []

class UserUpdate(schemas.BaseUserUpdate):
    """Schema for updating a user."""
    business_id: Optional[UUID] = None
    has_completed_survey: Optional[bool] = None
    roles: Optional[List[str]] = None

class Token(schemas.BaseModel):
    """Schema for token."""
    access_token: str
    token_type: str = "bearer"

class UserLogin(schemas.BaseModel):
    """Schema for user login."""
    username: str
    password: str

class UserBase(schemas.BaseUser):
    """Schema for user base."""
    pass

class UserResponse(UserBase):
    """Schema for user response."""
    id: str
    business_id: str
    roles: List[str]
    has_completed_survey: bool = False

    class Config:
        """Pydantic configuration."""
        from_attributes = True

class BusinessBase(schemas.BaseUser):
    """Schema for business base."""
    pass

class BusinessCreate(schemas.BaseUserCreate):
    """Schema for creating a new business."""
    admin_email: EmailStr
    admin_password: str

class BusinessResponse(schemas.BaseUser):
    """Schema for business response."""
    id: str
    customer_id: str

    class Config:
        """Pydantic configuration."""
        from_attributes = True

class RoleBase(schemas.BaseUser):
    """Schema for role base."""
    pass

class RoleCreate(schemas.BaseUserCreate):
    """Schema for creating a new role."""
    pass

class RoleResponse(schemas.BaseUser):
    """Schema for role response."""
    id: str

    class Config:
        """Pydantic configuration."""
        from_attributes = True 