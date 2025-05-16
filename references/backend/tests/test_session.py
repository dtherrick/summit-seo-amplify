"""Tests for session management system.

This module contains tests for:
- Session creation and validation
- Session middleware functionality
- Session cleanup and expiry
- Rate limiting
- Security headers
"""

import pytest
from datetime import datetime, timedelta
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from app.core.session import SessionManager, SessionData
from app.core.middleware.session import SessionMiddleware
from app.core.security_config import security_config
from app.main import app

@pytest.fixture
def mock_redis():
    """Mock Redis client for testing."""
    class MockRedis:
        def __init__(self):
            self.data = {}
            self.sets = {}
        
        async def setex(self, key, timeout, value):
            self.data[key] = value
        
        async def get(self, key):
            return self.data.get(key)
        
        async def delete(self, key):
            self.data.pop(key, None)
        
        async def sadd(self, key, value):
            if key not in self.sets:
                self.sets[key] = set()
            self.sets[key].add(value)
        
        async def srem(self, key, value):
            if key in self.sets:
                self.sets[key].discard(value)
        
        async def smembers(self, key):
            return list(self.sets.get(key, set()))
        
        async def scan(self, cursor, match=None, count=None):
            keys = [k for k in self.data.keys() if k.startswith(match.replace("*", ""))]
            return 0, keys
        
        async def incr(self, key):
            if key not in self.data:
                self.data[key] = 1
            else:
                self.data[key] = str(int(self.data[key]) + 1)
            return int(self.data[key])
        
        async def expire(self, key, timeout):
            pass
    
    return MockRedis()

@pytest.fixture
def session_manager(mock_redis):
    """Create SessionManager instance for testing."""
    return SessionManager(mock_redis)

@pytest.fixture
def mock_request():
    """Create mock Request object."""
    request = Mock()
    request.client.host = "127.0.0.1"
    request.headers = {"user-agent": "test-agent"}
    return request

@pytest.mark.asyncio
async def test_session_creation(session_manager, mock_request):
    """Test creating a new session."""
    user_id = "test-user"
    
    # Create session
    session_id = await session_manager.create_session(user_id, mock_request)
    assert session_id is not None
    
    # Get session
    session = await session_manager.get_session(session_id)
    assert session is not None
    assert session.user_id == user_id
    assert session.ip_address == "127.0.0.1"
    assert session.user_agent == "test-agent"
    assert session.is_active is True

@pytest.mark.asyncio
async def test_session_validation(session_manager, mock_request):
    """Test session validation and expiry."""
    user_id = "test-user"
    
    # Create session
    session_id = await session_manager.create_session(user_id, mock_request)
    
    # Test valid session
    is_valid = await session_manager.validate_session(session_id)
    assert is_valid is True
    
    # Test invalid session
    is_valid = await session_manager.validate_session("invalid-session")
    assert is_valid is False
    
    # Test expired session
    session = await session_manager.get_session(session_id)
    session.expires_at = datetime.utcnow() - timedelta(minutes=1)
    await session_manager.redis.setex(
        session_manager._get_key(session_id),
        60,
        session.json()
    )
    is_valid = await session_manager.validate_session(session_id)
    assert is_valid is False

@pytest.mark.asyncio
async def test_session_cleanup(session_manager, mock_request):
    """Test session cleanup functionality."""
    user_id = "test-user"
    
    # Create multiple sessions
    session_ids = []
    for _ in range(3):
        session_id = await session_manager.create_session(user_id, mock_request)
        session_ids.append(session_id)
    
    # Expire some sessions
    for session_id in session_ids[:2]:
        session = await session_manager.get_session(session_id)
        session.expires_at = datetime.utcnow() - timedelta(minutes=1)
        await session_manager.redis.setex(
            session_manager._get_key(session_id),
            60,
            session.json()
        )
    
    # Run cleanup
    cleaned = await session_manager.cleanup_expired_sessions()
    assert cleaned == 2
    
    # Verify remaining sessions
    sessions = await session_manager.get_user_sessions(user_id)
    assert len(sessions) == 1

@pytest.mark.asyncio
async def test_rate_limiting():
    """Test rate limiting middleware."""
    client = TestClient(app)
    
    # Make requests up to limit
    for _ in range(security_config.rate_limit_max_requests):
        response = client.get("/")
        assert response.status_code != 429
    
    # Make one more request
    response = client.get("/")
    assert response.status_code == 429
    assert response.json()["detail"] == "Too many requests"

def test_security_headers():
    """Test security headers middleware."""
    client = TestClient(app)
    response = client.get("/")
    
    # Check security headers
    headers = response.headers
    assert headers["X-Content-Type-Options"] == "nosniff"
    assert headers["X-Frame-Options"] == "DENY"
    assert headers["X-XSS-Protection"] == "1; mode=block"
    assert "Strict-Transport-Security" in headers
    assert "Content-Security-Policy" in headers

@pytest.mark.asyncio
async def test_session_middleware():
    """Test session middleware functionality."""
    app = FastAPI()
    app.add_middleware(SessionMiddleware)
    
    @app.get("/test")
    async def test_endpoint(request: Request):
        return {"session": request.state.session is not None}
    
    client = TestClient(app)
    
    # Test without session
    response = client.get("/test")
    assert response.status_code == 200
    
    # Test with invalid session
    response = client.get("/test", headers={"X-Session-ID": "invalid"})
    assert response.status_code == 401
    
    # Test excluded path
    response = client.get("/docs")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_user_sessions(session_manager, mock_request):
    """Test user session management."""
    user_id = "test-user"
    
    # Create multiple sessions
    session_ids = []
    for _ in range(3):
        session_id = await session_manager.create_session(user_id, mock_request)
        session_ids.append(session_id)
    
    # List sessions
    sessions = await session_manager.get_user_sessions(user_id)
    assert len(sessions) == 3
    
    # End specific session
    await session_manager.end_session(session_ids[0])
    sessions = await session_manager.get_user_sessions(user_id)
    assert len(sessions) == 2
    
    # End all sessions
    await session_manager.end_all_user_sessions(user_id)
    sessions = await session_manager.get_user_sessions(user_id)
    assert len(sessions) == 0 