"""Security configuration module.

This module provides centralized security configurations and utilities
for the application, including authentication, authorization, and
data protection settings.

The module includes:
- Security policy configurations
- Password validation rules
- Token security settings
- Rate limiting configurations
- Security headers

Example:
    ```python
    from app.core.security_config import (
        SecurityConfig,
        validate_password,
        get_security_headers
    )
    
    # Check password strength
    is_valid, errors = validate_password("user_password")
    
    # Get security headers
    headers = get_security_headers()
    ```
"""

from typing import Dict, List, Optional, Tuple
import re
from pydantic import BaseModel, Field
from fastapi import Request, Response
from fastapi.security import HTTPBearer
import secrets
from datetime import datetime, timedelta

from app.core.config import get_settings

settings = get_settings()

class SecurityConfig(BaseModel):
    """Security configuration settings.
    
    Attributes:
        min_password_length: Minimum password length
        require_special_char: Whether special characters are required
        require_number: Whether numbers are required
        require_uppercase: Whether uppercase letters are required
        require_lowercase: Whether lowercase letters are required
        max_login_attempts: Maximum failed login attempts
        lockout_duration: Account lockout duration in minutes
        jwt_expiry: JWT token expiry time in minutes
        refresh_token_expiry: Refresh token expiry time in days
        rate_limit_requests: Number of requests allowed per window
        rate_limit_window: Time window for rate limiting in seconds
    """
    
    min_password_length: int = 12
    require_special_char: bool = True
    require_number: bool = True
    require_uppercase: bool = True
    require_lowercase: bool = True
    max_login_attempts: int = 5
    lockout_duration: int = 15
    jwt_expiry: int = 30
    refresh_token_expiry: int = 7
    rate_limit_requests: int = 100
    rate_limit_window: int = 60
    
    class Config:
        """Pydantic model configuration."""
        frozen = True

# Create global security configuration
security_config = SecurityConfig()

# Security token bearer
security = HTTPBearer(
    scheme_name="JWT",
    description="JWT authentication token",
    auto_error=True
)

def validate_password(password: str) -> Tuple[bool, List[str]]:
    """Validate password strength against security policy.
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple[bool, List[str]]: (is_valid, list of validation errors)
        
    Example:
        ```python
        is_valid, errors = validate_password("user_password")
        if not is_valid:
            print("Password validation failed:", errors)
        ```
    """
    errors = []
    
    # Check length
    if len(password) < security_config.min_password_length:
        errors.append(
            f"Password must be at least {security_config.min_password_length} characters"
        )
    
    # Check for special character
    if security_config.require_special_char and not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append("Password must contain at least one special character")
    
    # Check for number
    if security_config.require_number and not re.search(r"\d", password):
        errors.append("Password must contain at least one number")
    
    # Check for uppercase
    if security_config.require_uppercase and not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter")
    
    # Check for lowercase
    if security_config.require_lowercase and not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter")
    
    return len(errors) == 0, errors

def get_security_headers() -> Dict[str, str]:
    """Get security headers for HTTP responses.
    
    Returns:
        Dict[str, str]: Security headers
        
    Example:
        ```python
        @app.middleware("http")
        async def add_security_headers(request: Request, call_next):
            response = await call_next(request)
            headers = get_security_headers()
            response.headers.update(headers)
            return response
        ```
    """
    return {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": (
            "default-src 'self'; "
            "img-src 'self' data: https:; "
            "style-src 'self' 'unsafe-inline' https:; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https:; "
            "connect-src 'self' https:; "
            "frame-ancestors 'none'"
        ),
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": (
            "accelerometer=(), "
            "camera=(), "
            "geolocation=(), "
            "gyroscope=(), "
            "magnetometer=(), "
            "microphone=(), "
            "payment=(), "
            "usb=()"
        )
    }

def generate_secure_token(length: int = 32) -> str:
    """Generate a cryptographically secure token.
    
    Args:
        length: Token length in bytes
        
    Returns:
        str: Secure token
        
    Example:
        ```python
        refresh_token = generate_secure_token(32)
        ```
    """
    return secrets.token_urlsafe(length)

def is_token_expired(expiry: datetime) -> bool:
    """Check if a token has expired.
    
    Args:
        expiry: Token expiry datetime
        
    Returns:
        bool: True if token has expired
        
    Example:
        ```python
        if is_token_expired(token.expiry):
            raise HTTPException(status_code=401, detail="Token expired")
        ```
    """
    return datetime.utcnow() > expiry

class RateLimiter:
    """Rate limiting utility.
    
    Attributes:
        requests: Maximum requests allowed
        window: Time window in seconds
        
    Example:
        ```python
        limiter = RateLimiter(100, 60)
        if not await limiter.is_allowed(request):
            raise HTTPException(status_code=429)
        ```
    """
    
    def __init__(
        self,
        requests: int = security_config.rate_limit_requests,
        window: int = security_config.rate_limit_window
    ):
        self.requests = requests
        self.window = window
    
    async def is_allowed(self, request: Request) -> bool:
        """Check if request is allowed under rate limit.
        
        Args:
            request: FastAPI request
            
        Returns:
            bool: True if request is allowed
        """
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Get Redis client
        redis = request.app.state.redis
        
        # Get current count
        key = f"rate_limit:{client_ip}"
        count = await redis.get(key)
        
        if count is None:
            # First request
            await redis.setex(key, self.window, 1)
            return True
        
        count = int(count)
        if count >= self.requests:
            return False
        
        # Increment count
        await redis.incr(key)
        return True 