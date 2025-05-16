"""Middleware module for the application.

This module provides middleware components for the FastAPI application, handling:
- CORS (Cross-Origin Resource Sharing)
- Trusted Host validation
- Request/Response logging
- Rate limiting
- Redis connection management

The middleware components in this module add important security, monitoring,
and performance features to the application.

Example:
    ```python
    from fastapi import FastAPI
    from app.core.middleware import setup_middleware, init_redis

    app = FastAPI()
    setup_middleware(app)

    @app.on_event("startup")
    async def startup():
        await init_redis()
    ```

Note:
    The rate limiting middleware requires a running Redis instance. Make sure
    Redis is properly configured in your environment variables.
"""
import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from loguru import logger
from redis.asyncio import Redis

from app.core.config import get_settings

settings = get_settings()

async def init_redis() -> Redis:
    """Initialize Redis connection for rate limiting.
    
    This function establishes a connection to Redis and initializes the
    FastAPI Limiter with this connection. It should be called during
    application startup.
    
    Returns:
        Redis: The initialized Redis client instance
    
    Raises:
        ConnectionError: If unable to connect to Redis
        
    Example:
        ```python
        @app.on_event("startup")
        async def startup():
            redis = await init_redis()
        ```
    """
    redis = Redis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True
    )
    await FastAPILimiter.init(redis)
    return redis

def setup_middleware(app: FastAPI) -> None:
    """Set up middleware components for the FastAPI application.
    
    This function adds various middleware components to the application:
    - CORS middleware for handling cross-origin requests
    - Trusted host middleware for security
    - Logging middleware for request/response tracking
    - Rate limiting middleware for API protection
    
    Args:
        app: The FastAPI application instance
    
    Example:
        ```python
        app = FastAPI()
        setup_middleware(app)
        ```
    """
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Trusted host middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"],  # Configure this based on your needs
    )

    # Add logging middleware
    @app.middleware("http")
    async def logging_middleware(
        request: Request,
        call_next: Callable,
    ) -> Response:
        """Log request and response details.
        
        This middleware logs information about incoming requests and their
        corresponding responses, including timing information.
        
        Args:
            request: The incoming HTTP request
            call_next: The next middleware or route handler
        
        Returns:
            Response: The HTTP response
            
        Note:
            This middleware uses the loguru logger, which should be
            configured according to your logging requirements.
        """
        start_time = time.time()
        
        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"Client: {request.client.host if request.client else 'Unknown'}"
        )
        
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response
        logger.info(
            f"Response: {response.status_code} "
            f"Process Time: {process_time:.2f}s"
        )
        
        return response

    # Add rate limiting middleware
    @app.middleware("http")
    async def rate_limit_middleware(
        request: Request,
        call_next: Callable,
    ) -> Response:
        """Apply rate limiting to API requests.
        
        This middleware applies rate limiting to all API routes. It uses
        Redis to track request counts and enforce limits.
        
        Args:
            request: The incoming HTTP request
            call_next: The next middleware or route handler
        
        Returns:
            Response: The HTTP response
            
        Note:
            Rate limiting is only applied to paths starting with "/api/".
            Configure the limits using RATE_LIMIT_TIMES and RATE_LIMIT_SECONDS
            in your settings.
        """
        if request.url.path.startswith("/api/"):
            limiter = RateLimiter(
                times=settings.RATE_LIMIT_TIMES,
                seconds=settings.RATE_LIMIT_SECONDS,
            )
            await limiter(request)
        
        return await call_next(request) 