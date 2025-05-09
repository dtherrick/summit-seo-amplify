"""Tenant API routes."""
import logging
import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ..models.tenant import Tenant, TenantCreate, TenantBase
from ..db.dynamodb import create_tenant, get_tenant
from ..utils.security import get_current_user, get_current_admin

logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

@router.get("/me", response_model=Tenant)
async def read_tenant_me(current_user: dict = Depends(get_current_user)):
    """Get the current user's tenant."""
    tenant_id = current_user.get("tenant_id")
    if not tenant_id:
        raise HTTPException(status_code=404, detail="Tenant not found for user")

    tenant = await get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    return tenant

@router.get("/{tenant_id}", response_model=Tenant)
async def read_tenant(
    tenant_id: str,
    current_user: dict = Depends(get_current_admin)
):
    """Get a tenant by ID (admin only)."""
    tenant = await get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant

@router.post("/", response_model=Tenant)
async def create_new_tenant(
    tenant: TenantCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new tenant."""
    # Generate a unique ID
    tenant_id = str(uuid.uuid4())

    # Create tenant object for database
    now = datetime.utcnow().isoformat()
    tenant_data = {
        "id": tenant_id,
        "owner_id": tenant.owner_id,
        "name": tenant.name,
        "business_email": tenant.business_email,
        "primary_website": str(tenant.primary_website) if tenant.primary_website else None,
        "industry": tenant.industry,
        "description": tenant.description,
        "created_at": now,
        "updated_at": now,
        "is_active": True,
        "subscription_tier": "free",
        "max_competitor_sites": 5  # Default limit for free tier
    }

    # Create the tenant in the database
    await create_tenant(tenant_data)

    return tenant_data