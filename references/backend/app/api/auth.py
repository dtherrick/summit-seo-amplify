"""Authentication router module.

This module provides authentication endpoints for user login,
logout, session management, and token refresh.
"""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Request, Response, HTTPException, status
from pydantic import BaseModel

from app.core.security_config import security_config
from app.core.validation import validate_password
from app.core.session import SessionManager
from app.models.user import User
from app.db.session import get_db
from app.core.auth import (
    create_access_token,
    get_password_hash,
    verify_password,
    get_current_user
)

router = APIRouter()

class LoginRequest(BaseModel):
    """Login request model."""
    email: str
    password: str
    remember_me: Optional[bool] = False

class LoginResponse(BaseModel):
    """Login response model."""
    access_token: str
    token_type: str = "bearer"
    expires_at: int
    user: User

@router.post("/login", response_model=LoginResponse)
async def login(
    request: Request,
    login_data: LoginRequest,
    db = Depends(get_db)
):
    """Log in a user.
    
    Args:
        request: The request object
        login_data: Login credentials
        db: Database session
        
    Returns:
        LoginResponse: Login response with access token and user data
        
    Raises:
        HTTPException: If login fails
    """
    # Get user by email
    user = await db.scalar(
        select(User).where(User.email == login_data.email)
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=(
            security_config.jwt_extended_expiry
            if login_data.remember_me
            else security_config.jwt_expiry
        )
    )
    
    # Create session
    session_manager = request.state.session_manager
    session_id = await session_manager.create_session(
        user_id=str(user.id),
        request=request
    )
    
    # Get session data
    session = await session_manager.get_session(session_id)
    
    # Set session cookie
    response = Response()
    response.set_cookie(
        "session_id",
        session_id,
        max_age=session.expires_at.timestamp() - datetime.utcnow().timestamp(),
        httponly=True,
        secure=True,
        samesite="strict"
    )
    
    return LoginResponse(
        access_token=access_token,
        expires_at=int(session.expires_at.timestamp()),
        user=user
    )

@router.post("/logout")
async def logout(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Log out a user.
    
    Args:
        request: The request object
        current_user: The current user
        
    Returns:
        dict: Success message
    """
    # End session
    session_manager = request.state.session_manager
    session_id = request.headers.get("X-Session-ID")
    if session_id:
        await session_manager.end_session(session_id)
    
    # Clear session cookie
    response = Response()
    response.delete_cookie("session_id")
    
    return {"message": "Successfully logged out"}

@router.post("/refresh")
async def refresh_token(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Refresh access token.
    
    Args:
        request: The request object
        current_user: The current user
        
    Returns:
        dict: New access token and expiry
    """
    # Create new access token
    access_token = create_access_token(
        data={"sub": str(current_user.id)}
    )
    
    # Get session
    session_manager = request.state.session_manager
    session_id = request.headers.get("X-Session-ID")
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No session found"
        )
    
    # Validate and refresh session
    is_valid = await session_manager.validate_session(session_id)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session"
        )
    
    # Get session data
    session = await session_manager.get_session(session_id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_at": int(session.expires_at.timestamp())
    }

@router.get("/sessions")
async def list_sessions(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """List active sessions for current user.
    
    Args:
        request: The request object
        current_user: The current user
        
    Returns:
        list: List of active sessions
    """
    session_manager = request.state.session_manager
    sessions = await session_manager.get_user_sessions(str(current_user.id))
    
    return [
        {
            "created_at": session.created_at.isoformat(),
            "expires_at": session.expires_at.isoformat(),
            "ip_address": session.ip_address,
            "user_agent": session.user_agent
        }
        for session in sessions
    ]

@router.post("/sessions/revoke-all")
async def revoke_all_sessions(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Revoke all sessions for current user.
    
    Args:
        request: The request object
        current_user: The current user
        
    Returns:
        dict: Success message
    """
    session_manager = request.state.session_manager
    await session_manager.end_all_user_sessions(str(current_user.id))
    
    return {"message": "All sessions revoked"} 