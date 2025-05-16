"""Tests for session analytics module.

This module contains tests for:
- Login event tracking
- Security event tracking
- Session statistics
- Anomaly detection
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from fastapi import Request
from collections import defaultdict

from app.core.analytics.session import (
    SessionAnalytics,
    LoginEvent,
    SecurityEvent,
    SessionStats
)

@pytest.fixture
def mock_redis():
    """Mock Redis client for testing."""
    class MockRedis:
        def __init__(self):
            self.data = {}
            self.lists = defaultdict(list)
            self.hashes = defaultdict(dict)
        
        async def lpush(self, key, value):
            self.lists[key].insert(0, value)
        
        async def lrange(self, key, start, stop):
            return self.lists[key][start:stop if stop != -1 else None]
        
        async def hincrby(self, key, field, amount):
            if key not in self.hashes:
                self.hashes[key] = {}
            if field not in self.hashes[key]:
                self.hashes[key][field] = 0
            self.hashes[key][field] += amount
            return self.hashes[key][field]
        
        async def hgetall(self, key):
            return self.hashes[key]
        
        async def pipeline(self):
            return self
        
        async def execute(self):
            return []
        
        async def scan(self, cursor, match=None, count=None):
            keys = [k for k in self.lists.keys() if k.startswith(match.replace("*", ""))]
            return 0, keys
        
        async def scard(self, key):
            return len(self.lists.get(key, []))
    
    return MockRedis()

@pytest.fixture
def mock_request():
    """Mock Request object."""
    request = Mock()
    request.client.host = "127.0.0.1"
    request.headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    return request

@pytest.fixture
def mock_geoip():
    """Mock GeoIP reader."""
    class MockLocation:
        def __init__(self):
            self.country = Mock(name="United States")
            self.city = Mock(name="New York")
    
    class MockReader:
        def city(self, ip):
            return MockLocation()
    
    return MockReader()

@pytest.mark.asyncio
async def test_track_login(mock_redis, mock_request):
    """Test tracking login events."""
    with patch("geoip2.database.Reader", return_value=mock_geoip()):
        analytics = SessionAnalytics(mock_redis)
        
        # Track successful login
        await analytics.track_login(
            "session-1",
            "user-1",
            mock_request,
            True
        )
        
        # Track failed login
        await analytics.track_login(
            "session-2",
            "user-1",
            mock_request,
            False
        )
        
        # Verify events
        events = await mock_redis.lrange("login_events:user-1", 0, -1)
        assert len(events) == 2
        
        # Verify stats
        stats = await mock_redis.hgetall("user_stats:user-1")
        assert int(stats["total_logins"]) == 2
        assert int(stats["successful_logins"]) == 1
        assert int(stats["failed_logins"]) == 1

@pytest.mark.asyncio
async def test_track_security_event(mock_redis, mock_request):
    """Test tracking security events."""
    analytics = SessionAnalytics(mock_redis)
    
    # Track security event
    await analytics.track_security_event(
        "suspicious_login",
        "session-1",
        "user-1",
        mock_request,
        {"reason": "unusual_location"}
    )
    
    # Verify event
    events = await mock_redis.lrange("security_events:user-1", 0, -1)
    assert len(events) == 1
    
    event = SecurityEvent.parse_raw(events[0])
    assert event.event_type == "suspicious_login"
    assert event.session_id == "session-1"
    assert event.details["reason"] == "unusual_location"

@pytest.mark.asyncio
async def test_get_user_stats(mock_redis, mock_request):
    """Test getting user statistics."""
    with patch("geoip2.database.Reader", return_value=mock_geoip()):
        analytics = SessionAnalytics(mock_redis)
        
        # Create some login events
        for i in range(5):
            await analytics.track_login(
                f"session-{i}",
                "user-1",
                mock_request,
                i < 3  # 3 successful, 2 failed
            )
        
        # Get stats
        stats = await analytics.get_user_stats("user-1")
        
        assert stats.total_sessions == 5
        assert stats.login_success_rate == 0.6  # 3/5
        assert "Windows" in stats.os
        assert "Chrome" in stats.browsers
        assert "United States" in stats.countries

@pytest.mark.asyncio
async def test_detect_anomalies(mock_redis, mock_request):
    """Test anomaly detection."""
    with patch("geoip2.database.Reader", return_value=mock_geoip()):
        analytics = SessionAnalytics(mock_redis)
        
        # Create normal login pattern
        for _ in range(5):
            await analytics.track_login(
                "session-1",
                "user-1",
                mock_request,
                True
            )
        
        # Test with same pattern
        anomalies = await analytics.detect_anomalies(
            "session-2",
            "user-1",
            mock_request
        )
        assert len(anomalies) == 0
        
        # Test with different user agent
        different_request = Mock()
        different_request.client.host = "127.0.0.1"
        different_request.headers = {
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"
        }
        
        anomalies = await analytics.detect_anomalies(
            "session-3",
            "user-1",
            different_request
        )
        assert len(anomalies) > 0
        assert any("device" in anomaly.lower() for anomaly in anomalies)

@pytest.mark.asyncio
async def test_get_security_events(mock_redis, mock_request):
    """Test retrieving security events."""
    analytics = SessionAnalytics(mock_redis)
    
    # Create some security events
    events = [
        ("suspicious_login", {"reason": "unusual_location"}),
        ("brute_force", {"attempts": 5}),
        ("session_hijack", {"evidence": "token_reuse"})
    ]
    
    for event_type, details in events:
        await analytics.track_security_event(
            event_type,
            "session-1",
            "user-1",
            mock_request,
            details
        )
    
    # Get events
    stored_events = await analytics.get_security_events("user-1")
    
    assert len(stored_events) == 3
    assert stored_events[0].event_type == "session_hijack"
    assert stored_events[1].event_type == "brute_force"
    assert stored_events[2].event_type == "suspicious_login" 