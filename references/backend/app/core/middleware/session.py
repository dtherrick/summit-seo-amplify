"""Session middleware for FastAPI.

This module provides middleware for managing user sessions in FastAPI applications.
It handles session validation, renewal, and cleanup.

Example:
    ```python
    from fastapi import FastAPI
    from app.core.middleware.session import SessionMiddleware
    
    app = FastAPI()
    app.add_middleware(SessionMiddleware)
    ```
"""

from typing import Optional, Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.core.session import SessionManager
from app.core.redis import get_redis
from app.core.config import get_settings

settings = get_settings()

class SessionMiddleware(BaseHTTPMiddleware):
    """Middleware for session management.
    
    This middleware handles:
    - Session validation
    - Session renewal
    - Session cleanup
    - Session headers
    
    Attributes:
        app: The ASGI application
        session_header: Name of the session header
        exclude_paths: List of paths to exclude from session management
    """
    
    def __init__(
        self,
        app: ASGIApp,
        session_header: str = "X-Session-ID",
        exclude_paths: Optional[list[str]] = None
    ):
        super().__init__(app)
        self.session_header = session_header
        self.exclude_paths = exclude_paths or [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/health",
            "/metrics"
        ]
    
    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        """Process the request/response cycle.
        
        Args:
            request: The incoming request
            call_next: The next middleware/endpoint
            
        Returns:
            Response: The response
        """
        # Skip session management for excluded paths
        if request.url.path in self.exclude_paths:
            return await call_next(request)
        
        # Get session ID from header
        session_id = request.headers.get(self.session_header)
        
        # Initialize session manager
        redis = await get_redis()
        session_manager = SessionManager(redis)
        
        # Store session manager in request state
        request.state.session_manager = session_manager
        
        if not session_id:
            # No session ID provided
            response = await call_next(request)
            return response
        
        # Validate session
        is_valid = await session_manager.validate_session(session_id)
        if not is_valid:
            # Invalid or expired session
            response = Response(
                status_code=401,
                content="Invalid or expired session"
            )
            return response
        
        # Get session data
        session = await session_manager.get_session(session_id)
        if not session:
            response = Response(
                status_code=401,
                content="Session not found"
            )
            return response
        
        # Store session data in request state
        request.state.session = session
        
        # Process request
        response = await call_next(request)
        
        # Add session headers to response
        response.headers[self.session_header] = session_id
        response.headers["X-Session-Expires"] = str(
            int(session.expires_at.timestamp())
        )
        
        return response 