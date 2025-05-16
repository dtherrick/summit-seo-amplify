"""Session management module.

This module provides secure session management functionality,
including session creation, validation, and cleanup.

The module includes:
- Session creation and validation
- Session timeout management
- Active session tracking
- Session cleanup utilities

Example:
    ```python
    from app.core.session import (
        SessionManager,
        create_session,
        validate_session
    )
    
    # Create new session
    session_id = await create_session(user_id)
    
    # Validate session
    is_valid = await validate_session(session_id)
    ```
"""

from typing import Optional, Dict, List
from datetime import datetime, timedelta
import json
from uuid import uuid4
from redis.asyncio import Redis
from fastapi import Request, HTTPException, status
from pydantic import BaseModel

from app.core.config import get_settings
from app.core.security_config import security_config

settings = get_settings()

class SessionData(BaseModel):
    """Session data model.
    
    Attributes:
        user_id: ID of the session user
        created_at: Session creation timestamp
        expires_at: Session expiration timestamp
        ip_address: Client IP address
        user_agent: Client user agent
        is_active: Whether the session is active
    """
    
    user_id: str
    created_at: datetime
    expires_at: datetime
    ip_address: str
    user_agent: str
    is_active: bool = True

class SessionManager:
    """Session management utility.
    
    This class provides methods for managing user sessions,
    including creation, validation, and cleanup.
    
    Attributes:
        redis: Redis client instance
        prefix: Prefix for session keys
        timeout: Session timeout in minutes
        
    Example:
        ```python
        session_manager = SessionManager(redis_client)
        session_id = await session_manager.create_session(user_id)
        ```
    """
    
    def __init__(
        self,
        redis: Redis,
        prefix: str = "session:",
        timeout: int = security_config.jwt_expiry
    ):
        self.redis = redis
        self.prefix = prefix
        self.timeout = timeout
    
    def _get_key(self, session_id: str) -> str:
        """Get Redis key for session."""
        return f"{self.prefix}{session_id}"
    
    async def create_session(
        self,
        user_id: str,
        request: Request
    ) -> str:
        """Create a new session.
        
        Args:
            user_id: User ID for the session
            request: FastAPI request object
            
        Returns:
            str: Session ID
            
        Example:
            ```python
            session_id = await manager.create_session(
                user_id="123",
                request=request
            )
            ```
        """
        # Generate session ID
        session_id = str(uuid4())
        
        # Create session data
        session = SessionData(
            user_id=user_id,
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(minutes=self.timeout),
            ip_address=request.client.host if request.client else "unknown",
            user_agent=request.headers.get("user-agent", "unknown")
        )
        
        # Store session in Redis
        await self.redis.setex(
            self._get_key(session_id),
            self.timeout * 60,  # Convert to seconds
            session.json()
        )
        
        # Add to user's active sessions
        await self.redis.sadd(
            f"user_sessions:{user_id}",
            session_id
        )
        
        return session_id
    
    async def get_session(self, session_id: str) -> Optional[SessionData]:
        """Get session data.
        
        Args:
            session_id: Session ID to retrieve
            
        Returns:
            Optional[SessionData]: Session data if found
            
        Example:
            ```python
            session = await manager.get_session(session_id)
            if session:
                print(f"User {session.user_id} is logged in")
            ```
        """
        data = await self.redis.get(self._get_key(session_id))
        if not data:
            return None
        
        return SessionData.parse_raw(data)
    
    async def validate_session(self, session_id: str) -> bool:
        """Validate session and update expiry.
        
        Args:
            session_id: Session ID to validate
            
        Returns:
            bool: True if session is valid
            
        Example:
            ```python
            if await manager.validate_session(session_id):
                await process_request()
            ```
        """
        session = await self.get_session(session_id)
        if not session:
            return False
        
        # Check if session is active and not expired
        if not session.is_active or datetime.utcnow() > session.expires_at:
            await self.end_session(session_id)
            return False
        
        # Update expiry
        session.expires_at = datetime.utcnow() + timedelta(minutes=self.timeout)
        await self.redis.setex(
            self._get_key(session_id),
            self.timeout * 60,
            session.json()
        )
        
        return True
    
    async def end_session(self, session_id: str) -> None:
        """End a session.
        
        Args:
            session_id: Session ID to end
            
        Example:
            ```python
            await manager.end_session(session_id)
            ```
        """
        # Get session data
        session = await self.get_session(session_id)
        if session:
            # Remove from user's active sessions
            await self.redis.srem(
                f"user_sessions:{session.user_id}",
                session_id
            )
        
        # Delete session
        await self.redis.delete(self._get_key(session_id))
    
    async def get_user_sessions(self, user_id: str) -> List[SessionData]:
        """Get all active sessions for a user.
        
        Args:
            user_id: User ID to get sessions for
            
        Returns:
            List[SessionData]: List of active sessions
            
        Example:
            ```python
            sessions = await manager.get_user_sessions(user_id)
            print(f"User has {len(sessions)} active sessions")
            ```
        """
        # Get session IDs
        session_ids = await self.redis.smembers(f"user_sessions:{user_id}")
        
        # Get session data
        sessions = []
        for session_id in session_ids:
            session = await self.get_session(session_id)
            if session and session.is_active:
                sessions.append(session)
        
        return sessions
    
    async def end_all_user_sessions(self, user_id: str) -> None:
        """End all sessions for a user.
        
        Args:
            user_id: User ID to end sessions for
            
        Example:
            ```python
            await manager.end_all_user_sessions(user_id)
            ```
        """
        # Get session IDs
        session_ids = await self.redis.smembers(f"user_sessions:{user_id}")
        
        # End each session
        for session_id in session_ids:
            await self.end_session(session_id)
        
        # Remove user's session set
        await self.redis.delete(f"user_sessions:{user_id}")
    
    async def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions.
        
        Returns:
            int: Number of sessions cleaned up
            
        Example:
            ```python
            cleaned = await manager.cleanup_expired_sessions()
            print(f"Cleaned up {cleaned} expired sessions")
            ```
        """
        count = 0
        cursor = 0
        pattern = f"{self.prefix}*"
        
        while True:
            cursor, keys = await self.redis.scan(
                cursor,
                match=pattern,
                count=100
            )
            
            for key in keys:
                data = await self.redis.get(key)
                if data:
                    session = SessionData.parse_raw(data)
                    if datetime.utcnow() > session.expires_at:
                        session_id = key.decode().replace(self.prefix, "")
                        await self.end_session(session_id)
                        count += 1
            
            if cursor == 0:
                break
        
        return count 