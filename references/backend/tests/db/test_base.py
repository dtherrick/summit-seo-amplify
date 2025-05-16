"""Tests for the database base module.

This module contains tests for database connection,
session management, and model base functionality.
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

from app.db.base import Base, get_db, init_db
from app.core.config import settings

pytestmark = pytest.mark.asyncio

async def test_get_db():
    """Test database session creation and cleanup."""
    async for session in get_db():
        assert isinstance(session, AsyncSession)
        # Test that session is usable
        result = await session.execute("SELECT 1")
        assert result.scalar() == 1

async def test_init_db():
    """Test database initialization."""
    # Create a test engine with NullPool to ensure clean shutdown
    engine = create_async_engine(
        settings.TEST_DATABASE_URL,
        poolclass=NullPool,
        echo=False
    )
    
    # Initialize database
    await init_db(engine)
    
    # Verify tables are created
    async with engine.begin() as conn:
        # Get list of tables
        result = await conn.execute(
            """
            SELECT tablename 
            FROM pg_catalog.pg_tables 
            WHERE schemaname != 'pg_catalog' 
            AND schemaname != 'information_schema'
            """
        )
        tables = result.scalars().all()
        
        # Check that our model tables exist
        model_tables = {t.name for t in Base.metadata.tables.values()}
        for table in model_tables:
            assert table in tables
    
    # Cleanup
    async with engine.begin() as conn:
        await conn.execute('DROP SCHEMA public CASCADE')
        await conn.execute('CREATE SCHEMA public')
    await engine.dispose()

async def test_session_rollback():
    """Test session rollback on error."""
    async for session in get_db():
        # Start a transaction
        async with session.begin():
            # Execute a valid query
            await session.execute("SELECT 1")
            
            # Try to execute an invalid query
            with pytest.raises(Exception):
                await session.execute("INVALID SQL")
            
            # Transaction should be rolled back automatically

        # Session should still be usable after rollback
        result = await session.execute("SELECT 1")
        assert result.scalar() == 1

async def test_concurrent_sessions():
    """Test concurrent database sessions."""
    async def access_db():
        async for session in get_db():
            result = await session.execute("SELECT 1")
            assert result.scalar() == 1
            return True
    
    # Run multiple concurrent database accesses
    results = await pytest.asyncio.gather(
        *[access_db() for _ in range(5)]
    )
    assert all(results)

async def test_session_isolation():
    """Test session transaction isolation."""
    # Create two sessions
    sessions = [get_db(), get_db()]
    async for session1, session2 in zip(*sessions):
        # Start transaction in first session
        async with session1.begin():
            # Create a temporary table
            await session1.execute(
                """
                CREATE TEMPORARY TABLE test_isolation 
                (id serial PRIMARY KEY, value text)
                """
            )
            await session1.execute(
                """
                INSERT INTO test_isolation (value) 
                VALUES ('test')
                """
            )
            
            # Second session should not see the temporary table
            # until transaction is committed
            with pytest.raises(Exception):
                await session2.execute(
                    "SELECT * FROM test_isolation"
                )
        
        # After commit, second session should see the table
        result = await session2.execute(
            "SELECT value FROM test_isolation"
        )
        assert result.scalar() == "test"
        
        # Cleanup
        await session2.execute("DROP TABLE test_isolation")

async def test_base_model_reflection():
    """Test SQLAlchemy model reflection capabilities."""
    # Get all models that inherit from Base
    models = Base._decl_class_registry.values()
    
    for model in models:
        if hasattr(model, "__tablename__"):
            # Verify model has primary key
            assert hasattr(model, "__table__")
            assert model.__table__.primary_key
            
            # Verify model has created_at and updated_at
            assert hasattr(model, "created_at")
            assert hasattr(model, "updated_at")

async def test_engine_pool_settings():
    """Test database engine pool settings."""
    engine = create_async_engine(
        settings.TEST_DATABASE_URL,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW
    )
    
    # Verify pool settings
    assert engine.pool.size() == settings.DB_POOL_SIZE
    assert engine.pool._max_overflow == settings.DB_MAX_OVERFLOW
    
    await engine.dispose() 