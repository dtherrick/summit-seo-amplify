"""Test configuration and fixtures for the FastAPI application.

This module provides pytest fixtures for testing the FastAPI application,
including database setup, test client configuration, and test data.

Features:
- Async test database setup and teardown
- Test client configuration
- Authentication fixtures
- Test data factories

Example:
    ```python
    async def test_my_endpoint(client: AsyncClient, user_token: str):
        response = await client.get(
            "/api/v1/endpoint",
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert response.status_code == 200
    ```
"""

import asyncio
import pytest
from typing import AsyncGenerator, Dict
from uuid import UUID
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)

from app.core.config import settings
from app.db.base import Base
from app.main import app
from app.core.security import create_jwt_token
from app.api.deps import get_db

# Test database URL
TEST_DATABASE_URL = settings.DATABASE_URL + "_test"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def engine():
    """Create a test database engine.
    
    This fixture creates a fresh test database for each session,
    manages the database schema, and handles cleanup.
    """
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def db_session(engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database session for a test.
    
    This fixture creates a new session for each test,
    rolls back changes after the test completes.
    """
    session_maker = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False
    )
    
    async with session_maker() as session:
        yield session
        await session.rollback()

@pytest.fixture
async def client(db_session) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client for the FastAPI application.
    
    This fixture provides an HTTP client for testing API endpoints,
    configured with the test database session.
    """
    async def _get_test_db():
        yield db_session

    app.dependency_overrides[get_db] = _get_test_db
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()

@pytest.fixture
async def test_business(db_session) -> Dict:
    """Create a test business in the database.
    
    Returns:
        dict: The created business data
    """
    business_id = UUID(int=1)
    business_data = {
        "id": business_id,
        "name": "Test Business",
        "description": "A business for testing",
        "is_active": True
    }
    
    # Here you would use your business model to create the test business
    # For now, we'll just return the test data
    return business_data

@pytest.fixture
async def test_user(db_session) -> Dict:
    """Create a test user in the database.
    
    Returns:
        dict: The created user data
    """
    user_id = UUID(int=1)
    user_data = {
        "id": user_id,
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "is_active": True,
        "is_superuser": False,
        "business_id": UUID(int=1)  # Link to test business
    }
    
    # Here you would use your user model to create the test user
    # For now, we'll just return the test data
    return user_data

@pytest.fixture
async def test_superuser(db_session) -> Dict:
    """Create a test superuser in the database.
    
    Returns:
        dict: The created superuser data
    """
    user_id = UUID(int=2)
    user_data = {
        "id": user_id,
        "email": "admin@example.com",
        "first_name": "Admin",
        "last_name": "User",
        "is_active": True,
        "is_superuser": True
    }
    
    # Here you would use your user model to create the test superuser
    # For now, we'll just return the test data
    return user_data

@pytest.fixture
def user_token(test_user: Dict) -> str:
    """Create a JWT token for a regular test user.
    
    Args:
        test_user: The test user data
    
    Returns:
        str: JWT token for authentication
    """
    return create_jwt_token({"sub": str(test_user["id"])})

@pytest.fixture
def superuser_token(test_superuser: Dict) -> str:
    """Create a JWT token for a test superuser.
    
    Args:
        test_superuser: The test superuser data
    
    Returns:
        str: JWT token for authentication
    """
    return create_jwt_token({"sub": str(test_superuser["id"])}) 