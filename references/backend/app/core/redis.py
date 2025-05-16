"""Redis connection and caching module.

This module provides Redis connection management and caching utilities
for the application. It includes:
- Redis connection pool management
- Caching decorators
- Key management utilities
"""

from functools import wraps
from typing import Any, Callable, Optional, TypeVar
import json
from redis.asyncio import Redis, ConnectionPool, ConnectionError
from loguru import logger

from .config import get_settings

settings = get_settings()

# Type variable for generic function decorators
F = TypeVar('F', bound=Callable[..., Any])

# Global Redis pool
redis_pool: Optional[ConnectionPool] = None

async def init_redis_pool() -> None:
    """Initialize Redis connection pool.
    
    This function should be called during application startup.
    """
    global redis_pool
    try:
        redis_pool = ConnectionPool.from_url(
            settings.REDIS_URL,
            max_connections=settings.REDIS_MAX_CONNECTIONS,
            decode_responses=True
        )
        logger.info("Redis connection pool initialized successfully")
    except Exception as e:
        logger.error(f"Failed to create Redis connection pool: {e}")
        redis_pool = None

async def close_redis_pool() -> None:
    """Close Redis connection pool.
    
    This function should be called during application shutdown.
    """
    global redis_pool
    if redis_pool:
        await redis_pool.disconnect()
        redis_pool = None
        logger.info("Redis connection pool closed")

async def get_redis() -> Optional[Redis]:
    """Get Redis connection from pool.
    
    Returns:
        Optional[Redis]: Redis connection instance if available, None otherwise
    """
    if not redis_pool:
        logger.warning("Redis connection pool not available")
        return None
    
    try:
        return Redis(connection_pool=redis_pool)
    except ConnectionError as e:
        logger.error(f"Failed to get Redis connection: {e}")
        return None

def cache_key(prefix: str, *args: Any, **kwargs: Any) -> str:
    """Generate cache key from prefix and arguments.
    
    Args:
        prefix: Key prefix
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        str: Generated cache key
    """
    key_parts = [prefix]
    if args:
        key_parts.extend(str(arg) for arg in args)
    if kwargs:
        key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
    return ":".join(key_parts)

def cached(
    prefix: str,
    ttl: int = 300,
    key_func: Optional[Callable[..., str]] = None
) -> Callable[[F], F]:
    """Decorator for caching function results in Redis.
    
    Args:
        prefix: Cache key prefix
        ttl: Time to live in seconds
        key_func: Optional function to generate cache key
        
    Returns:
        Callable: Decorated function
    """
    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            redis = await get_redis()
            if not redis:
                # If Redis is not available, just execute the function
                return await func(*args, **kwargs)
            
            # Generate cache key
            if key_func:
                key = key_func(*args, **kwargs)
            else:
                key = cache_key(prefix, *args, **kwargs)
            
            # Try to get from cache
            try:
                cached_value = await redis.get(key)
                if cached_value:
                    try:
                        return json.loads(cached_value)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to decode cached value for key: {key}")
            except Exception as e:
                logger.error(f"Failed to get cached value for key {key}: {e}")
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            try:
                await redis.setex(
                    key,
                    ttl,
                    json.dumps(result)
                )
            except Exception as e:
                logger.error(f"Failed to cache result for key {key}: {e}")
            
            return result
        return wrapper
    return decorator

async def invalidate_cache(prefix: str, *args: Any, **kwargs: Any) -> None:
    """Invalidate cache entries matching prefix and arguments.
    
    Args:
        prefix: Cache key prefix
        *args: Positional arguments
        **kwargs: Keyword arguments
    """
    redis = await get_redis()
    if not redis:
        return
        
    pattern = cache_key(prefix, *args, **kwargs) + "*"
    
    try:
        # Get all matching keys
        keys = await redis.keys(pattern)
        if keys:
            await redis.delete(*keys)
            logger.debug(f"Invalidated {len(keys)} cache entries for pattern: {pattern}")
    except Exception as e:
        logger.error(f"Failed to invalidate cache for pattern {pattern}: {e}") 