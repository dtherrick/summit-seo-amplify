"""Authentication and authorization module.

This module provides authentication and authorization functionality for the application,
including user authentication, role-based access control, and business access verification.
It integrates with FastAPI's security system and SQLAlchemy for database access.

The module provides:
- User authentication using JWT tokens
- Role-based access control
- Business access verification
- Dependency functions for protected routes

Example:
    ```python
    from fastapi import Depends, FastAPI
    from app.core.auth import get_current_user, RoleChecker

    app = FastAPI()
    allow_business_admin = RoleChecker(["business_admin"])

    @app.get("/protected")
    async def protected_route(user = Depends(get_current_user)):
        return {"message": f"Hello {user.email}"}

    @app.get("/admin-only")
    async def admin_route(user = Depends(allow_business_admin)):
        return {"message": "Hello admin"}
    ```

Note:
    This module assumes the existence of User and Role models in the database,
    and requires proper JWT token configuration in the security module.
"""
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from ..models.auth import User, Role, Session as UserSession
from ..core.security import decode_access_token
from ..db.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/jwt/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get the current authenticated user from the JWT token.
    
    This dependency function authenticates the current request using the JWT token
    and retrieves the corresponding user from the database.

    Args:
        token: JWT token from the request (automatically extracted by FastAPI)
        db: Database session dependency

    Returns:
        User: The authenticated user instance

    Raises:
        HTTPException: If token is invalid or user is not found/inactive

    Example:
        ```python
        @app.get("/me")
        async def read_users_me(
            current_user: User = Depends(get_current_user)
        ):
            return current_user
        ```

    Note:
        This function checks both token validity and user status (active/inactive)
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decode the token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    # Get user ID from payload
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # Get user from database
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return user

async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """Check if the current user is an active superuser.
    
    This dependency function verifies that the current user has superuser role.

    Args:
        current_user: The current authenticated user (from get_current_user)

    Returns:
        User: The authenticated superuser

    Raises:
        HTTPException: If user doesn't have superuser role

    Example:
        ```python
        @app.get("/admin")
        async def admin_route(
            admin: User = Depends(get_current_active_superuser)
        ):
            return {"message": "Hello superuser"}
        ```
    """
    if not any(role.role == "superuser" for role in current_user.roles):
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges"
        )
    return current_user

def check_business_access(user: User, business_id: str) -> bool:
    """Check if a user has access to a specific business.
    
    Verifies whether a user has permission to access a business based on
    their roles and business association.

    Args:
        user: The user to check
        business_id: The ID of the business to check access for

    Returns:
        bool: True if user has access, False otherwise

    Example:
        ```python
        @app.get("/business/{business_id}")
        async def get_business(
            business_id: str,
            user: User = Depends(get_current_user)
        ):
            if not check_business_access(user, business_id):
                raise HTTPException(status_code=403)
            return {"message": "Access granted"}
        ```

    Note:
        Superusers have access to all businesses. Regular users can only
        access their assigned business.
    """
    # Superusers can access all businesses
    if any(role.role == "superuser" for role in user.roles):
        return True
    
    # Users can only access their own business
    return str(user.business_id) == business_id

class RoleChecker:
    """Role-based access control checker.
    
    This class creates a dependency callable that checks if a user
    has any of the specified roles.

    Attributes:
        allowed_roles: List of role names that are allowed access

    Example:
        ```python
        allow_admin = RoleChecker(["admin", "superuser"])

        @app.get("/admin-only")
        async def admin_route(user = Depends(allow_admin)):
            return {"message": "Hello admin"}
        ```
    """

    def __init__(self, allowed_roles: list[str]):
        """Initialize the role checker.
        
        Args:
            allowed_roles: List of role names that should be allowed access
        """
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)) -> User:
        """Check if the user has any of the allowed roles.
        
        This method is called by FastAPI's dependency injection system.

        Args:
            user: The current authenticated user

        Returns:
            User: The user if they have appropriate role

        Raises:
            HTTPException: If user doesn't have any of the allowed roles
        """
        for role in user.roles:
            if role.role in self.allowed_roles:
                return user
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges"
        ) 