from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text
from loguru import logger
from .config import get_settings

settings = get_settings()

# Use the async database URL from settings
engine = create_async_engine(settings.async_database_url)
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
Base = declarative_base()

async def init_db() -> None:
    """Initialize database connection.
    
    This function should be called during application startup.
    """
    try:
        # Test the connection
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            await conn.commit()
        logger.info("Database connection initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database connection: {e}")
        raise

async def close_db() -> None:
    """Close database connection.
    
    This function should be called during application shutdown.
    """
    try:
        await engine.dispose()
        logger.info("Database connection closed")
    except Exception as e:
        logger.error(f"Failed to close database connection: {e}")

# Dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close() 