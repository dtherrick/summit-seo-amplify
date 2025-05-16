"""FastAPI Users configuration module.

This module provides user management functionality using FastAPI Users library,
including authentication, registration, and user operations. It implements JWT-based
authentication with bearer token transport.

The module sets up:
- User manager for handling user operations
- JWT-based authentication backend
- User database integration with SQLAlchemy
- FastAPI Users instance with configured backends

Example:
    ```python
    from fastapi import Depends, FastAPI
    from app.core.users import fastapi_users, auth_backend
    
    app = FastAPI()
    
    # Add authentication routes
    app.include_router(
        fastapi_users.get_auth_router(auth_backend),
        prefix="/auth/jwt",
        tags=["auth"]
    )
    
    # Protected route example
    @app.get("/protected")
    def protected_route(user = Depends(fastapi_users.current_user)):
        return {"message": f"Hello {user.email}"}
    ```

Note:
    This module requires proper configuration of JWT secrets and user manager
    secrets in the application settings. Ensure these are set securely in
    production environments.
"""
from typing import Optional
from uuid import UUID

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.db.base import get_async_session
from app.models.user import User

settings = get_settings()

class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    """User manager for FastAPI Users.
    
    This class handles user management operations such as registration,
    password reset, and email verification. It extends FastAPI Users'
    BaseUserManager with UUID-based user identification.

    Attributes:
        reset_password_token_secret (str): Secret for password reset tokens
        verification_token_secret (str): Secret for email verification tokens

    Example:
        ```python
        user_manager = UserManager(user_db)
        
        # Register a new user
        user = await user_manager.create(
            UserCreate(email="user@example.com", password="password")
        )
        ```

    Note:
        The manager uses the same secret for both password reset and
        verification tokens. In a production environment, consider using
        separate secrets for enhanced security.
    """
    
    reset_password_token_secret = settings.USER_MANAGER_SECRET
    verification_token_secret = settings.USER_MANAGER_SECRET

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        """Handle post-registration tasks.
        
        This method is called automatically after a successful user registration.
        Currently implements basic logging; extend this method to add custom
        post-registration logic (e.g., welcome emails, profile setup).

        Args:
            user: The newly registered user instance
            request: Optional FastAPI request object that triggered the registration

        Note:
            This is an async method and can perform I/O operations without
            blocking the main thread.
        """
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ) -> None:
        """Handle forgot password tasks.
        
        This method is called automatically after a password reset is requested.
        Currently implements basic logging; extend this method to add custom
        logic (e.g., sending reset password emails).

        Args:
            user: The user requesting password reset
            token: The generated password reset token
            request: Optional FastAPI request object that triggered the request

        Note:
            In production, avoid logging the actual token and implement
            secure token delivery (e.g., via email).
        """
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ) -> None:
        """Handle verification request tasks.
        
        This method is called automatically after an email verification is requested.
        Currently implements basic logging; extend this method to add custom
        logic (e.g., sending verification emails).

        Args:
            user: The user requesting verification
            token: The generated verification token
            request: Optional FastAPI request object that triggered the request

        Note:
            In production, avoid logging the actual token and implement
            secure token delivery (e.g., via email).
        """
        print(f"Verification requested for user {user.id}. Verification token: {token}")

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Get user database dependency.
    
    Creates and yields a SQLAlchemy user database instance for dependency injection.

    Args:
        session: An async SQLAlchemy session from the session dependency

    Yields:
        SQLAlchemyUserDatabase: Database adapter for user operations

    Example:
        ```python
        @app.get("/users")
        async def get_users(user_db = Depends(get_user_db)):
            return await user_db.list()
        ```
    """
    yield SQLAlchemyUserDatabase(session, User)

async def get_user_manager(user_db=Depends(get_user_db)):
    """Get user manager dependency.
    
    Creates and yields a UserManager instance for dependency injection.

    Args:
        user_db: A user database instance from the user_db dependency

    Yields:
        UserManager: Manager instance for user operations

    Example:
        ```python
        @app.post("/custom-register")
        async def custom_register(
            user_manager = Depends(get_user_manager),
            user_create: UserCreate
        ):
            return await user_manager.create(user_create)
        ```
    """
    yield UserManager(user_db)

# Bearer transport for JWT
bearer_transport = BearerTransport(tokenUrl="api/v1/auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    """Get JWT strategy.
    
    Creates a JWT strategy instance with configured secret and lifetime.

    Returns:
        JWTStrategy: Strategy instance for JWT handling

    Note:
        The JWT secret and lifetime are configured through application
        settings. Ensure these are properly set for your environment.
    """
    return JWTStrategy(
        secret=settings.JWT_SECRET,
        lifetime_seconds=settings.JWT_LIFETIME_SECONDS,
    )

# Authentication backend
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# FastAPI Users instance
fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
) 