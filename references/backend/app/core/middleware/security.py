"""Security middleware module.

This module provides middleware for integrating security
features into the FastAPI application, including:
- Step-up authentication
- Device fingerprinting
- Location-based security
- Rate limiting
"""

from typing import Callable, Dict, Optional
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.core.security.step_up import StepUpAuth
from app.core.security.device import DeviceManager
from app.core.security.brute_force import BruteForceProtection
from app.core.redis import get_redis
from app.core.config import get_settings

settings = get_settings()

class SecurityMiddleware(BaseHTTPMiddleware):
    """Security middleware for FastAPI.
    
    Integrates various security features into the request
    processing pipeline.
    """
    
    def __init__(
        self,
        app: ASGIApp,
        exclude_paths: Optional[list[str]] = None
    ):
        super().__init__(app)
        self.exclude_paths = exclude_paths or []
        self.redis = None
        self.step_up = None
        self.device = None
        self.brute_force = None
    
    async def _init_components(self):
        """Initialize security components."""
        if not self.redis:
            self.redis = await get_redis()
            if not self.redis:
                raise RuntimeError("Failed to initialize Redis client")
            self.step_up = StepUpAuth(self.redis)
            self.device = DeviceManager(self.redis)
            self.brute_force = BruteForceProtection(self.redis)
    
    async def _should_process(self, request: Request) -> bool:
        """Check if request should be processed.
        
        Args:
            request: FastAPI request object
            
        Returns:
            bool: Whether request should be processed
        """
        path = request.url.path
        return not any(
            path.startswith(exclude_path)
            for exclude_path in self.exclude_paths
        )
    
    async def _get_user_id(self, request: Request) -> Optional[str]:
        """Get user ID from request.
        
        Args:
            request: FastAPI request object
            
        Returns:
            Optional[str]: User ID if found
        """
        # Get user ID from token
        token = request.headers.get("Authorization", "").split(" ")[-1]
        if not token:
            return None
        
        # TODO: Get user ID from token
        # This should be implemented based on your token
        # validation logic
        return None
    
    async def _check_brute_force(
        self,
        request: Request,
        user_id: Optional[str]
    ) -> Optional[Response]:
        """Check for brute force attempts.
        
        Args:
            request: FastAPI request object
            user_id: User ID if available
            
        Returns:
            Optional[Response]: Error response if blocked
        """
        status = await self.brute_force.get_status(
            user_id,
            request.client.host
        )
        
        if status.is_blocked:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Too many attempts. "
                    f"Try again in {status.wait_time} seconds."
                }
            )
        
        return None
    
    async def _check_device(
        self,
        request: Request,
        user_id: str
    ) -> Optional[Response]:
        """Check device security status.
        
        Args:
            request: FastAPI request object
            user_id: User ID
            
        Returns:
            Optional[Response]: Error response if verification needed
        """
        device_info = await self.device.process_device(request, user_id)
        
        if not device_info.is_trusted:
            # Get available step-up methods
            methods = await self.step_up.get_available_methods(user_id)
            
            if not methods:
                return JSONResponse(
                    status_code=403,
                    content={
                        "detail": "Device not trusted. "
                        "Please set up additional authentication methods."
                    }
                )
            
            return JSONResponse(
                status_code=428,
                content={
                    "detail": "Additional verification required.",
                    "methods": methods,
                    "device_info": {
                        "fingerprint": device_info.fingerprint,
                        "location": device_info.location,
                        "trust_score": device_info.trust_score
                    }
                }
            )
        
        return None
    
    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        """Process request through security middleware.
        
        Args:
            request: FastAPI request object
            call_next: Next middleware/endpoint
            
        Returns:
            Response: HTTP response
        """
        # Initialize components if needed
        await self._init_components()
        
        if not await self._should_process(request):
            return await call_next(request)
        
        # Get user ID if available
        user_id = await self._get_user_id(request)
        
        # Check for brute force attempts
        if response := await self._check_brute_force(request, user_id):
            return response
        
        # For authenticated endpoints
        if user_id:
            # Check device security
            if response := await self._check_device(request, user_id):
                return response
        
        # Process request
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        
        return response 