"""Tenant model definitions."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, HttpUrl

class TenantBase(BaseModel):
    """Base tenant model."""
    name: str
    business_email: EmailStr
    primary_website: Optional[HttpUrl] = None
    industry: Optional[str] = None
    description: Optional[str] = None

class TenantCreate(TenantBase):
    """Tenant creation model."""
    owner_id: str  # Reference to the user who created the tenant

class TenantInDB(TenantBase):
    """Tenant model as stored in the database."""
    id: str
    owner_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_active: bool = True
    subscription_tier: str = "free"  # Options: "free", "basic", "premium"
    max_competitor_sites: int = 5  # Default limit for free tier

class Tenant(TenantInDB):
    """API tenant model."""
    pass