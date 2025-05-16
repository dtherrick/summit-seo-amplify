"""API optimization module.

This module provides optimization utilities for API responses,
including response caching, compression, and serialization optimization.

The module includes:
- Response caching with Redis
- Response compression
- Efficient pagination
- Payload optimization

Example:
    ```python
    from fastapi import FastAPI
    from app.core.optimization import (
        setup_response_optimization,
        cache_response,
        optimize_pagination
    )

    app = FastAPI()
    setup_response_optimization(app)

    @app.get("/items")
    @cache_response(timeout=300)
    async def list_items(
        pagination = Depends(optimize_pagination())
    ):
        return {"items": get_items(**pagination)}
    ```
"""

from functools import wraps
from typing import Any, Callable, Dict, Optional, TypeVar, Union
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.middleware.gzip import GZipMiddleware
from redis.asyncio import Redis
import json
import zlib
from loguru import logger

from app.core.config import get_settings

settings = get_settings()

# Type variable for generic function decorators
F = TypeVar('F', bound=Callable[..., Any])

def setup_response_optimization(app: FastAPI) -> None:
    """Set up response optimization for FastAPI application.
    
    Configures:
    - Response compression
    - JSON serialization optimization
    - Response caching middleware
    
    Args:
        app: FastAPI application instance
        
    Example:
        ```python
        app = FastAPI()
        setup_response_optimization(app)
        ```
    """
    # Add Gzip compression
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Add response caching middleware
    @app.middleware("http")
    async def cache_middleware(request: Request, call_next: Callable) -> Response:
        # Skip caching for non-GET requests
        if request.method != "GET":
            return await call_next(request)
        
        # Get cache key from request
        cache_key = f"response_cache:{request.url.path}:{hash(str(request.query_params))}"
        
        # Get Redis client
        redis = Redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
        
        # Try to get cached response
        cached = await redis.get(cache_key)
        if cached:
            data = json.loads(cached)
            return JSONResponse(content=data)
        
        # Get response and cache it
        response = await call_next(request)
        if response.status_code == 200:
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk
            
            try:
                data = json.loads(response_body)
                await redis.setex(cache_key, 300, json.dumps(data))
            except json.JSONDecodeError:
                pass
        
        return response

def cache_response(
    timeout: int = 300,
    key_prefix: str = "response_cache"
) -> Callable[[F], F]:
    """Decorator to cache API response in Redis.
    
    Args:
        timeout: Cache timeout in seconds
        key_prefix: Prefix for cache keys
        
    Returns:
        Callable: Decorated function
        
    Example:
        ```python
        @app.get("/stats")
        @cache_response(timeout=300)
        async def get_stats():
            return {"total": calculate_stats()}
        ```
    """
    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Create cache key from function name and arguments
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args))}"
            
            # Get Redis client
            redis = Redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            
            # Try to get cached response
            cached = await redis.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Execute function and cache response
            result = await func(*args, **kwargs)
            await redis.setex(
                cache_key,
                timeout,
                json.dumps(jsonable_encoder(result))
            )
            
            return result
        return wrapper  # type: ignore
    return decorator

def optimize_pagination(
    default_limit: int = 20,
    max_limit: int = 100
) -> Callable[[Optional[int], Optional[int]], Dict[str, int]]:
    """Create an optimized pagination dependency.
    
    Args:
        default_limit: Default number of items per page
        max_limit: Maximum allowed limit
        
    Returns:
        Callable: FastAPI dependency function
        
    Example:
        ```python
        @app.get("/items")
        async def list_items(
            pagination = Depends(optimize_pagination())
        ):
            return get_items(**pagination)
        ```
    """
    def pagination(
        skip: Optional[int] = None,
        limit: Optional[int] = None
    ) -> Dict[str, int]:
        # Validate and optimize pagination parameters
        if skip is None or skip < 0:
            skip = 0
        
        if limit is None:
            limit = default_limit
        elif limit > max_limit:
            limit = max_limit
        elif limit < 1:
            limit = default_limit
        
        return {"skip": skip, "limit": limit}
    
    return pagination

def compress_payload(data: Union[dict, list, str]) -> bytes:
    """Compress data payload using zlib.
    
    Args:
        data: Data to compress
        
    Returns:
        bytes: Compressed data
        
    Example:
        ```python
        compressed = compress_payload(large_data_dict)
        ```
    """
    if isinstance(data, (dict, list)):
        data = json.dumps(data)
    return zlib.compress(data.encode())

def decompress_payload(data: bytes) -> Union[dict, list, str]:
    """Decompress zlib compressed data.
    
    Args:
        data: Compressed data
        
    Returns:
        Union[dict, list, str]: Decompressed data
        
    Example:
        ```python
        original = decompress_payload(compressed_data)
        ```
    """
    decompressed = zlib.decompress(data).decode()
    try:
        return json.loads(decompressed)
    except json.JSONDecodeError:
        return decompressed 