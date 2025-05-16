"""Database optimization module.

This module provides optimization settings and utilities for database operations,
including connection pooling, query caching, and performance monitoring.

The module includes:
- Optimized engine configuration
- Query result caching with Redis
- Statement compilation caching
- Query execution statistics
- Connection pool monitoring

Example:
    ```python
    from app.db.optimizations import (
        get_optimized_engine,
        cache_query_result,
        monitor_pool_status
    )

    # Create optimized engine
    engine = get_optimized_engine()

    # Cache query result
    @cache_query_result(timeout=300)
    async def get_user_stats():
        return await db.execute(stats_query)
    ```
"""

from functools import wraps
import time
from typing import Any, Callable, Optional, TypeVar
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from redis.asyncio import Redis
import json
import pickle
from loguru import logger

from app.core.config import get_settings

settings = get_settings()

# Type variable for generic function decorators
F = TypeVar('F', bound=Callable[..., Any])

def get_optimized_engine() -> AsyncEngine:
    """Create an optimized SQLAlchemy engine.
    
    Configures the engine with optimized settings for performance:
    - Connection pooling
    - Statement cache
    - Pool monitoring
    - Query timing
    
    Returns:
        AsyncEngine: Configured SQLAlchemy engine
        
    Example:
        ```python
        engine = get_optimized_engine()
        ```
    """
    engine = create_async_engine(
        settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
        echo=settings.DB_ECHO,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_timeout=30,  # Seconds to wait for pool connection
        pool_recycle=1800,  # Recycle connections after 30 minutes
        pool_pre_ping=True,  # Verify connections before use
        echo_pool=True,  # Log pool events
        future=True,
        # Query execution options
        execution_options={
            "compiled_cache": None,  # Enable statement cache
            "logging_token": "sql",  # For query logging
        }
    )
    
    # Add query timing logging
    @event.listens_for(engine.sync_engine, "before_cursor_execute")
    def before_cursor_execute(
        conn, cursor, statement, parameters, context, executemany
    ):
        conn.info.setdefault('query_start_time', []).append(time.time())

    @event.listens_for(engine.sync_engine, "after_cursor_execute")
    def after_cursor_execute(
        conn, cursor, statement, parameters, context, executemany
    ):
        total = time.time() - conn.info['query_start_time'].pop()
        logger.debug(f"Query execution time: {total:.3f}s")
    
    return engine

def cache_query_result(
    timeout: int = 300,
    key_prefix: str = "query_cache"
) -> Callable[[F], F]:
    """Decorator to cache query results in Redis.
    
    Args:
        timeout: Cache timeout in seconds
        key_prefix: Prefix for cache keys
        
    Returns:
        Callable: Decorated function
        
    Example:
        ```python
        @cache_query_result(timeout=300)
        async def get_user_stats():
            return await db.execute(stats_query)
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
            
            # Try to get cached result
            cached = await redis.get(cache_key)
            if cached:
                return pickle.loads(cached)
            
            # Execute query and cache result
            result = await func(*args, **kwargs)
            await redis.setex(
                cache_key,
                timeout,
                pickle.dumps(result)
            )
            
            return result
        return wrapper  # type: ignore
    return decorator

async def monitor_pool_status(engine: AsyncEngine) -> dict:
    """Monitor database connection pool status.
    
    Args:
        engine: SQLAlchemy engine to monitor
        
    Returns:
        dict: Pool statistics
        
    Example:
        ```python
        stats = await monitor_pool_status(engine)
        print(f"Active connections: {stats['size']}")
        ```
    """
    pool = engine.pool
    return {
        "size": pool.size(),
        "checked_out": pool.checkedout(),
        "overflow": pool.overflow(),
        "checkedin": pool.checkedin(),
    }

async def clear_query_cache(
    pattern: str = "query_cache:*",
    redis: Optional[Redis] = None
) -> int:
    """Clear cached query results matching pattern.
    
    Args:
        pattern: Pattern to match cache keys
        redis: Optional Redis client instance
        
    Returns:
        int: Number of keys cleared
        
    Example:
        ```python
        cleared = await clear_query_cache("query_cache:user_*")
        print(f"Cleared {cleared} cache entries")
        ```
    """
    if redis is None:
        redis = Redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
    
    # Get matching keys
    keys = await redis.keys(pattern)
    if not keys:
        return 0
    
    # Delete keys
    return await redis.delete(*keys) 