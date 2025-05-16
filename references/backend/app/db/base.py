"""Database configuration module.

This module provides the core database configuration for the application,
including async SQLAlchemy setup, session management, and the base model class.
It uses SQLAlchemy's async features for better performance and scalability.

The module sets up:
- Async database engine with connection pooling
- Session factory for managing database sessions
- Base class for declarative models
- Dependency function for FastAPI integration

Example:
    ```python
    from fastapi import Depends
    from app.db.base import Base, get_async_session
    from sqlalchemy.ext.asyncio import AsyncSession

    class User(Base):
        __tablename__ = "users"
        # ... model definition ...

    async def get_user(
        session: AsyncSession = Depends(get_async_session),
        user_id: int
    ):
        return await session.get(User, user_id)
    ```

Note:
    This module requires the PostgreSQL driver (asyncpg) and proper database
    configuration in the settings. Make sure the database URL and connection
    pool settings are properly configured.
"""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings

settings = get_settings()

# Create async engine with optimized configuration
engine = create_async_engine(
    settings.async_database_url,
    echo=settings.DB_ECHO,  # SQL query logging
    future=True,  # Enable future SQLAlchemy features
    pool_size=settings.DB_POOL_SIZE,  # Maximum number of connections in the pool
    max_overflow=settings.DB_MAX_OVERFLOW,  # Maximum overflow connections
    pool_pre_ping=True,  # Enable connection health checks
)

# Create async session factory with optimized settings
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit
    autoflush=False,  # Don't auto-flush changes (better control)
)

class Base(DeclarativeBase):
    """Base class for all database models.
    
    This class serves as the declarative base for SQLAlchemy models in the
    application. All model classes should inherit from this base class to
    ensure consistent configuration and behavior.

    Example:
        ```python
        from app.db.base import Base

        class User(Base):
            __tablename__ = "users"
            
            id = Column(Integer, primary_key=True)
            name = Column(String)
        ```

    Note:
        This class uses SQLAlchemy's new DeclarativeBase system, which
        provides better type checking and IDE support compared to the
        older declarative_base() function.
    """

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Create and yield an async database session.
    
    This dependency function creates a new async database session and yields
    it for use in FastAPI endpoints. The session is automatically closed
    when the request is complete, ensuring proper resource cleanup.

    Yields:
        AsyncSession: An async SQLAlchemy session for database operations

    Raises:
        SQLAlchemyError: If there are database connection issues

    Example:
        ```python
        from fastapi import Depends
        from sqlalchemy.ext.asyncio import AsyncSession

        async def get_user(session: AsyncSession = Depends(get_async_session)):
            result = await session.execute(select(User))
            return result.scalar_one_or_none()
        ```

    Note:
        This function should be used with FastAPI's dependency injection
        system. It ensures proper session management and cleanup, even
        if exceptions occur during request processing.
    """
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close() 