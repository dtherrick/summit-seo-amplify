"""Business management router module.

This module provides the API endpoints for managing businesses in the application.
It handles CRUD operations for businesses and includes role-based access control.

The module uses FastAPI's dependency injection system for:
- Database session management
- User authentication
- Role-based authorization

Key Features:
- Business CRUD operations
- User-business relationship management
- Role-based access control
- Async database operations

API Endpoints:
- GET /businesses - List all businesses (superuser only)
- POST /businesses - Create a new business (superuser only)
- GET /businesses/{id} - Get business details (superuser or business user)
- PATCH /businesses/{id} - Update business details (superuser only)
- DELETE /businesses/{id} - Delete a business (superuser only)

Example:
    ```python
    from fastapi import FastAPI
    from app.api.v1.business import router as business_router

    app = FastAPI()
    app.include_router(business_router, prefix="/api/v1")

    # Example usage with httpx client:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8000/api/v1/businesses",
            headers={"Authorization": f"Bearer {token}"}
        )
        businesses = response.json()
    ```

Note:
    All endpoints require authentication. Most operations are restricted to superusers,
    while some read operations are available to authenticated business users for their
    own business data.
"""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.users import fastapi_users
from app.db.base import get_async_session
from app.models.user import Business, User
from app.schemas.business import (
    BusinessCreate,
    BusinessRead,
    BusinessUpdate,
    BusinessWithUsers,
)

router = APIRouter(prefix="/businesses", tags=["businesses"])

# Authentication dependencies
current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)

async def get_business_or_404(
    business_id: UUID,
    session: AsyncSession = Depends(get_async_session),
) -> Business:
    """Retrieve a business by ID or raise a 404 error.

    This dependency function fetches a business from the database and ensures
    it exists before allowing the endpoint to proceed.

    Args:
        business_id: The UUID of the business to retrieve
        session: The database session (injected by FastAPI)

    Returns:
        Business: The found business instance

    Raises:
        HTTPException: 404 error if business is not found

    Example:
        ```python
        @router.get("/{business_id}")
        async def get_business(
            business: Business = Depends(get_business_or_404)
        ):
            return business
        ```

    Note:
        This is a FastAPI dependency that can be reused across multiple endpoints
        to ensure consistent 404 handling for business lookups.
    """
    result = await session.execute(
        select(Business).where(Business.id == business_id)
    )
    business = result.scalar_one_or_none()
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found",
        )
    return business

@router.get("", response_model=List[BusinessRead])
async def list_businesses(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
) -> List[Business]:
    """List all businesses in the system.

    This endpoint is restricted to superusers and returns all businesses
    registered in the system.

    Args:
        session: The database session (injected by FastAPI)
        user: The current superuser (injected by FastAPI)

    Returns:
        List[Business]: A list of all businesses

    Raises:
        HTTPException: 401 if user is not authenticated
        HTTPException: 403 if user is not a superuser

    Example:
        ```python
        # With authenticated client
        response = await client.get("/api/v1/businesses")
        businesses = response.json()
        ```

    Note:
        This endpoint might return a large dataset for systems with many
        businesses. Consider implementing pagination for production use.
    """
    result = await session.execute(select(Business))
    return result.scalars().all()

@router.post("", response_model=BusinessRead, status_code=status.HTTP_201_CREATED)
async def create_business(
    business_data: BusinessCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
) -> Business:
    """Create a new business.

    This endpoint allows superusers to create new businesses in the system.
    The business data is validated using the BusinessCreate model.

    Args:
        business_data: The business data to create
        session: The database session (injected by FastAPI)
        user: The current superuser (injected by FastAPI)

    Returns:
        Business: The newly created business

    Raises:
        HTTPException: 401 if user is not authenticated
        HTTPException: 403 if user is not a superuser
        ValidationError: If business_data fails validation

    Example:
        ```python
        # With authenticated client
        response = await client.post(
            "/api/v1/businesses",
            json={"name": "Acme Corp", "description": "A company"}
        )
        new_business = response.json()
        ```
    """
    business = Business(**business_data.model_dump())
    session.add(business)
    await session.commit()
    await session.refresh(business)
    return business

@router.get("/{business_id}", response_model=BusinessWithUsers)
async def get_business(
    business: Business = Depends(get_business_or_404),
    user: User = Depends(current_active_user),
) -> Business:
    """Get detailed information about a specific business.

    This endpoint returns detailed business information, including associated users.
    Access is restricted to superusers and users belonging to the business.

    Args:
        business: The business to retrieve (injected by get_business_or_404)
        user: The current authenticated user (injected by FastAPI)

    Returns:
        Business: The business details with associated users

    Raises:
        HTTPException: 401 if user is not authenticated
        HTTPException: 403 if user doesn't have access to this business
        HTTPException: 404 if business is not found

    Example:
        ```python
        # With authenticated client
        response = await client.get(f"/api/v1/businesses/{business_id}")
        business = response.json()
        ```
    """
    # Check if user has access to this business
    if not user.is_superuser and user.business_id != business.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this business",
        )
    return business

@router.patch("/{business_id}", response_model=BusinessRead)
async def update_business(
    business_data: BusinessUpdate,
    business: Business = Depends(get_business_or_404),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
) -> Business:
    """Update a business's information.

    This endpoint allows superusers to update business details.
    Only provided fields will be updated (partial updates supported).

    Args:
        business_data: The business data to update
        business: The business to update (injected by get_business_or_404)
        session: The database session (injected by FastAPI)
        user: The current superuser (injected by FastAPI)

    Returns:
        Business: The updated business

    Raises:
        HTTPException: 401 if user is not authenticated
        HTTPException: 403 if user is not a superuser
        HTTPException: 404 if business is not found
        ValidationError: If business_data fails validation

    Example:
        ```python
        # With authenticated client
        response = await client.patch(
            f"/api/v1/businesses/{business_id}",
            json={"name": "New Name"}
        )
        updated_business = response.json()
        ```
    """
    for field, value in business_data.model_dump(exclude_unset=True).items():
        setattr(business, field, value)
    
    await session.commit()
    await session.refresh(business)
    return business

@router.delete("/{business_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_business(
    business: Business = Depends(get_business_or_404),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
) -> None:
    """Delete a business.

    This endpoint allows superusers to delete a business from the system.
    This operation cannot be undone.

    Args:
        business: The business to delete (injected by get_business_or_404)
        session: The database session (injected by FastAPI)
        user: The current superuser (injected by FastAPI)

    Raises:
        HTTPException: 401 if user is not authenticated
        HTTPException: 403 if user is not a superuser
        HTTPException: 404 if business is not found

    Example:
        ```python
        # With authenticated client
        response = await client.delete(f"/api/v1/businesses/{business_id}")
        assert response.status_code == 204
        ```

    Note:
        This operation will also delete all associated data due to
        database cascade settings.
    """
    await session.delete(business)
    await session.commit() 