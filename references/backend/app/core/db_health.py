"""Database health check module.

This module provides functionality to verify and monitor database connectivity.
It includes utilities for checking database health and dependencies for
FastAPI routes that require database availability.

The module provides:
- Simple database connection verification
- FastAPI dependency for ensuring database availability
- Logging of database connection issues

Example:
    ```python
    from fastapi import FastAPI, Depends
    from app.core.db_health import verify_database_connected

    app = FastAPI()

    @app.get("/health")
    async def health_check(db_connected: bool = Depends(verify_database_connected)):
        return {"status": "healthy", "database": "connected"}
    ```

Note:
    This module uses SQLAlchemy's connection pooling, so connection checks
    are efficient and don't create new connections unnecessarily.
"""
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from typing import AsyncGenerator
import logging

from .database import engine

logger = logging.getLogger(__name__)

async def check_database_connection() -> bool:
    """Verify database connectivity without modifying schema.
    
    Performs a lightweight check of database connectivity by executing
    a simple SELECT query. This check doesn't modify any data or schema.

    Returns:
        bool: True if connection is successful, False otherwise

    Example:
        ```python
        is_connected = await check_database_connection()
        if not is_connected:
            logger.error("Database is not available")
        ```

    Note:
        This function logs any connection errors but doesn't raise exceptions,
        making it suitable for health checks.
    """
    try:
        # Use a simple SELECT 1 query that doesn't modify anything
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            return True
    except SQLAlchemyError as e:
        logger.error(f"Database connection failed: {str(e)}")
        return False

async def verify_database_connected() -> AsyncGenerator[bool, None]:
    """FastAPI dependency for ensuring database connectivity.
    
    This dependency function checks database connectivity before processing
    requests. It can be used to ensure routes only execute when the database
    is available.

    Yields:
        bool: True if database is connected

    Raises:
        HTTPException: With 503 status if database is not available

    Example:
        ```python
        @app.get("/data")
        async def get_data(
            db_connected: bool = Depends(verify_database_connected)
        ):
            # Database is guaranteed to be connected here
            return {"data": "some data"}
        ```

    Note:
        This is an async generator function suitable for FastAPI's
        dependency injection system. It will prevent route execution
        if the database is not available.
    """
    if not await check_database_connection():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )
    yield True 