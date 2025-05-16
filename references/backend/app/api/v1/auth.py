"""Authentication router module.

This module sets up the authentication and user management routes using FastAPI Users.
It provides a comprehensive set of endpoints for user authentication, registration,
password management, and user profile management.

The module includes routes for:
- JWT Authentication (login/logout)
- User Registration
- Password Reset
- Email Verification
- User Profile Management

API Endpoints:
- POST /auth/jwt/login - Login with username/password
- POST /auth/jwt/logout - Logout (revoke token)
- POST /auth/register - Register new user
- POST /auth/request-verify-token - Request email verification
- POST /auth/verify - Verify email
- POST /auth/forgot-password - Request password reset
- POST /auth/reset-password - Reset password
- GET /auth/users/me - Get current user profile
- PATCH /auth/users/me - Update current user profile

Example:
    ```python
    from fastapi import FastAPI
    from app.api.v1.auth import router as auth_router

    app = FastAPI()
    app.include_router(auth_router, prefix="/api/v1")

    # Example usage with httpx client:
    async with httpx.AsyncClient() as client:
        # Login
        response = await client.post(
            "http://localhost:8000/api/v1/auth/jwt/login",
            data={"username": "user@example.com", "password": "secret"}
        )
        token = response.json()["access_token"]

        # Get user profile
        response = await client.get(
            "http://localhost:8000/api/v1/auth/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        user = response.json()
    ```

Note:
    This module uses FastAPI Users for authentication and user management.
    The JWT authentication backend is configured in the core.users module.
    Email verification and password reset require proper email configuration.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.core.users import auth_backend, fastapi_users
from app.schemas.auth import UserCreate, UserRead, UserUpdate
from app.models.user import User
from app.db.base import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["auth"])

# JWT Authentication routes (login/logout)
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["auth"],
)

# User registration routes
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    tags=["auth"],
)

# Password reset routes
router.include_router(
    fastapi_users.get_reset_password_router(),
    tags=["auth"],
)

# Email verification routes
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    tags=["auth"],
)

# User profile management routes (including /me endpoint)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
) 