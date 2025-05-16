"""Tests for security features.

This module contains tests for:
- Step-up authentication
- Device fingerprinting
- Location-based security
- Brute force protection
- Security middleware
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.testclient import TestClient

from app.core.security.step_up import StepUpAuth, StepUpMethod
from app.core.security.device import DeviceManager, DeviceInfo
from app.core.security.brute_force import BruteForceProtection
from app.core.middleware.security import SecurityMiddleware

# Test data
TEST_USER_ID = "test-user-123"
TEST_FINGERPRINT = "test-device-456"
TEST_IP = "192.168.1.1"
TEST_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

@pytest.fixture
def mock_redis():
    """Mock Redis client."""
    return Mock()

@pytest.fixture
def step_up_auth(mock_redis):
    """Step-up authentication instance."""
    return StepUpAuth(mock_redis)

@pytest.fixture
def device_security(mock_redis):
    """Device security instance."""
    return DeviceManager(mock_redis)

@pytest.fixture
def brute_force(mock_redis):
    """Brute force protection instance."""
    return BruteForceProtection(mock_redis)

@pytest.fixture
def test_app():
    """Test FastAPI application."""
    app = FastAPI()
    app.add_middleware(
        SecurityMiddleware,
        exclude_paths=["/health"]
    )
    
    @app.get("/protected")
    async def protected_endpoint():
        return {"message": "success"}
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}
    
    return app

@pytest.fixture
def test_client(test_app):
    """Test client."""
    return TestClient(test_app)

@pytest.mark.asyncio
async def test_step_up_totp(step_up_auth):
    """Test TOTP setup and verification."""
    # Set up TOTP
    setup_data = await step_up_auth.setup_totp(TEST_USER_ID)
    assert "secret" in setup_data
    assert "uri" in setup_data
    
    # Mock stored method
    method = StepUpMethod(
        type="totp",
        enabled=True,
        data={"secret": setup_data["secret"]},
        last_used=None
    )
    step_up_auth.redis.hget.return_value = method.json()
    
    # Test verification
    import pyotp
    totp = pyotp.TOTP(setup_data["secret"])
    code = totp.now()
    
    is_valid = await step_up_auth.verify_totp(TEST_USER_ID, code)
    assert is_valid

@pytest.mark.asyncio
async def test_device_fingerprinting(device_security):
    """Test device fingerprinting and trust scoring."""
    # Mock request
    request = Mock()
    request.headers = {
        "user-agent": TEST_USER_AGENT,
        "accept": "*/*",
        "accept-language": "en-US",
        "accept-encoding": "gzip"
    }
    request.client.host = TEST_IP
    
    # Mock location data
    device_security._get_location = Mock(return_value={
        "country": "United States",
        "city": "New York",
        "latitude": "40.7128",
        "longitude": "-74.0060"
    })
    
    # Process new device
    device_info = await device_security.process_device(request, TEST_USER_ID)
    assert isinstance(device_info, DeviceInfo)
    assert not device_info.is_trusted
    assert device_info.trust_score == 0.5
    
    # Mock existing device
    stored_device = DeviceInfo(
        fingerprint=device_info.fingerprint,
        user_agent=TEST_USER_AGENT,
        ip_address=TEST_IP,
        location=device_info.location,
        first_seen=datetime.utcnow() - timedelta(days=31),
        last_seen=datetime.utcnow(),
        trust_score=0.9,
        is_trusted=True
    )
    device_security.redis.hget.return_value = stored_device.json()
    
    # Process existing device
    device_info = await device_security.process_device(request, TEST_USER_ID)
    assert device_info.is_trusted
    assert device_info.trust_score > 0.7

@pytest.mark.asyncio
async def test_brute_force_protection(brute_force):
    """Test brute force protection."""
    # Record failed attempts
    for _ in range(3):
        await brute_force.record_attempt(
            TEST_USER_ID,
            TEST_IP,
            success=False
        )
    
    # Check status
    status = await brute_force.get_status(TEST_USER_ID, TEST_IP)
    assert not status.is_blocked
    assert status.attempts == 3
    
    # Record more failures
    for _ in range(7):
        await brute_force.record_attempt(
            TEST_USER_ID,
            TEST_IP,
            success=False
        )
    
    # Check blocked status
    status = await brute_force.get_status(TEST_USER_ID, TEST_IP)
    assert status.is_blocked
    assert status.wait_time > 0
    
    # Record successful attempt
    await brute_force.record_attempt(
        TEST_USER_ID,
        TEST_IP,
        success=True
    )
    
    # Check reset status
    status = await brute_force.get_status(TEST_USER_ID, TEST_IP)
    assert not status.is_blocked
    assert status.attempts == 0

def test_security_middleware_excluded_path(test_client):
    """Test security middleware path exclusion."""
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_security_middleware_protected_path():
    """Test security middleware on protected path."""
    app = FastAPI()
    
    # Mock security components
    mock_step_up = Mock()
    mock_device = Mock()
    mock_brute_force = Mock()
    
    # Configure middleware
    middleware = SecurityMiddleware(app)
    middleware.step_up = mock_step_up
    middleware.device = mock_device
    middleware.brute_force = mock_brute_force
    
    # Mock request
    request = Mock()
    request.url.path = "/protected"
    request.headers = {"Authorization": "Bearer test-token"}
    request.client.host = TEST_IP
    
    # Mock brute force check
    mock_brute_force.get_status.return_value = Mock(
        is_blocked=False,
        attempts=0,
        wait_time=0
    )
    
    # Mock device check
    mock_device.process_device.return_value = Mock(
        is_trusted=True,
        fingerprint=TEST_FINGERPRINT,
        trust_score=0.9
    )
    
    # Test middleware
    async def mock_call_next(request):
        return JSONResponse(content={"message": "success"})
    
    response = await middleware.dispatch(request, mock_call_next)
    
    assert response.status_code == 200
    assert "X-Content-Type-Options" in response.headers
    assert "X-Frame-Options" in response.headers
    assert "X-XSS-Protection" in response.headers
    assert "Strict-Transport-Security" in response.headers

@pytest.mark.asyncio
async def test_security_middleware_untrusted_device():
    """Test security middleware with untrusted device."""
    app = FastAPI()
    middleware = SecurityMiddleware(app)
    
    # Mock request
    request = Mock()
    request.url.path = "/protected"
    request.headers = {"Authorization": "Bearer test-token"}
    request.client.host = TEST_IP
    
    # Mock device check
    mock_device_info = DeviceInfo(
        fingerprint=TEST_FINGERPRINT,
        user_agent=TEST_USER_AGENT,
        ip_address=TEST_IP,
        location=None,
        first_seen=datetime.utcnow(),
        last_seen=datetime.utcnow(),
        trust_score=0.4,
        is_trusted=False
    )
    
    middleware.device.process_device.return_value = mock_device_info
    middleware.step_up.get_available_methods.return_value = ["totp", "recovery"]
    
    # Test middleware
    async def mock_call_next(request):
        return JSONResponse(content={"message": "success"})
    
    response = await middleware.dispatch(request, mock_call_next)
    
    assert response.status_code == 428
    content = response.json()
    assert "methods" in content
    assert "device_info" in content
    assert content["methods"] == ["totp", "recovery"] 