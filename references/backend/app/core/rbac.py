"""Role-based access control (RBAC) module.

This module provides role-based access control functionality,
including role definitions, permission management, and access
verification utilities.

The module includes:
- Role definitions and hierarchies
- Permission management
- Access control decorators
- Role verification utilities

Example:
    ```python
    from fastapi import Depends
    from app.core.rbac import (
        requires_role,
        verify_business_access,
        Roles
    )
    
    @app.delete("/business/{business_id}")
    @requires_role([Roles.ADMIN, Roles.BUSINESS_OWNER])
    async def delete_business(
        business_id: int,
        user = Depends(get_current_user)
    ):
        await verify_business_access(user, business_id)
        return await delete_business_by_id(business_id)
    ```
"""

from enum import Enum
from typing import List, Optional, Set
from fastapi import Depends, HTTPException, status
from functools import wraps

from app.models.user import User
from app.models.business import Business
from app.db.base import AsyncSession, get_async_session

class Roles(str, Enum):
    """User role definitions.
    
    Attributes:
        ADMIN: System administrator
        BUSINESS_OWNER: Business owner
        BUSINESS_STAFF: Business staff member
        USER: Regular user
    """
    
    ADMIN = "admin"
    BUSINESS_OWNER = "business_owner"
    BUSINESS_STAFF = "business_staff"
    USER = "user"

class Permissions(str, Enum):
    """Permission definitions.
    
    Attributes:
        READ: Read access
        WRITE: Write access
        DELETE: Delete access
        MANAGE: Management access
    """
    
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    MANAGE = "manage"

# Role hierarchy and permissions
ROLE_HIERARCHY = {
    Roles.ADMIN: {
        Permissions.READ,
        Permissions.WRITE,
        Permissions.DELETE,
        Permissions.MANAGE
    },
    Roles.BUSINESS_OWNER: {
        Permissions.READ,
        Permissions.WRITE,
        Permissions.MANAGE
    },
    Roles.BUSINESS_STAFF: {
        Permissions.READ,
        Permissions.WRITE
    },
    Roles.USER: {
        Permissions.READ
    }
}

def requires_role(allowed_roles: List[Roles]):
    """Decorator to enforce role-based access control.
    
    Args:
        allowed_roles: List of roles allowed to access the endpoint
        
    Returns:
        Callable: Decorated function
        
    Example:
        ```python
        @app.post("/admin/users")
        @requires_role([Roles.ADMIN])
        async def create_user(user_data: UserCreate):
            return await create_new_user(user_data)
        ```
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get current user from kwargs
            user = kwargs.get("user")
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated"
                )
            
            # Check if user has required role
            if not any(role in allowed_roles for role in user.roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def has_permission(
    user: User,
    permission: Permissions,
    business_id: Optional[int] = None
) -> bool:
    """Check if user has specific permission.
    
    Args:
        user: User to check
        permission: Required permission
        business_id: Optional business ID for business-specific permissions
        
    Returns:
        bool: True if user has permission
        
    Example:
        ```python
        if has_permission(user, Permissions.WRITE, business_id=1):
            await update_business_data(business_id, data)
        ```
    """
    # Admin has all permissions
    if Roles.ADMIN in user.roles:
        return True
    
    # Check role permissions
    for role in user.roles:
        if permission in ROLE_HIERARCHY[role]:
            # For business-specific permissions, verify business access
            if business_id is not None:
                return user.business_id == business_id
            return True
    
    return False

async def verify_business_access(
    user: User,
    business_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> None:
    """Verify user has access to specific business.
    
    Args:
        user: User to verify
        business_id: Business ID to check
        session: Database session
        
    Raises:
        HTTPException: If user doesn't have access
        
    Example:
        ```python
        await verify_business_access(user, business_id)
        ```
    """
    # Admin has access to all businesses
    if Roles.ADMIN in user.roles:
        return
    
    # Check if user is associated with business
    business = await session.get(Business, business_id)
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Business not found"
        )
    
    if business.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access to this business not allowed"
        )

def get_user_permissions(user: User) -> Set[Permissions]:
    """Get all permissions for a user.
    
    Args:
        user: User to get permissions for
        
    Returns:
        Set[Permissions]: Set of user permissions
        
    Example:
        ```python
        permissions = get_user_permissions(user)
        if Permissions.MANAGE in permissions:
            await perform_management_action()
        ```
    """
    permissions = set()
    for role in user.roles:
        permissions.update(ROLE_HIERARCHY[role])
    return permissions

async def verify_action_allowed(
    user: User,
    permission: Permissions,
    business_id: Optional[int] = None,
    session: Optional[AsyncSession] = None
) -> None:
    """Verify if user is allowed to perform an action.
    
    Args:
        user: User to verify
        permission: Required permission
        business_id: Optional business ID
        session: Optional database session
        
    Raises:
        HTTPException: If action is not allowed
        
    Example:
        ```python
        await verify_action_allowed(
            user,
            Permissions.WRITE,
            business_id=1
        )
        ```
    """
    if not has_permission(user, permission, business_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Action not allowed"
        )
    
    if business_id and session:
        await verify_business_access(user, business_id, session) 