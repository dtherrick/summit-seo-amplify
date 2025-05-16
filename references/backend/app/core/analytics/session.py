"""Session analytics and monitoring module.

This module provides functionality for tracking and analyzing
user sessions, including:
- Login patterns
- Device analytics
- Geographic distribution
- Security events
- Usage statistics

Example:
    ```python
    from app.core.analytics.session import SessionAnalytics
    
    # Track login event
    await analytics.track_login(session_id, user_id, request)
    
    # Get user session stats
    stats = await analytics.get_user_stats(user_id)
    ```
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
from fastapi import Request
from pydantic import BaseModel
from redis.asyncio import Redis
import user_agents
from geoip2.database import Reader
from collections import defaultdict

from app.core.config import get_settings
from app.core.session import SessionData

settings = get_settings()

class LoginEvent(BaseModel):
    """Login event data model."""
    session_id: str
    user_id: str
    timestamp: datetime
    ip_address: str
    user_agent: str
    device_type: str
    browser: str
    os: str
    country: Optional[str]
    city: Optional[str]
    success: bool

class SecurityEvent(BaseModel):
    """Security event data model."""
    event_type: str
    session_id: str
    user_id: str
    timestamp: datetime
    ip_address: str
    details: Dict

class SessionStats(BaseModel):
    """Session statistics model."""
    total_sessions: int
    active_sessions: int
    devices: Dict[str, int]
    browsers: Dict[str, int]
    countries: Dict[str, int]
    average_session_duration: float
    login_success_rate: float

class SessionAnalytics:
    """Session analytics manager.
    
    This class provides methods for tracking and analyzing
    user sessions and security events.
    
    Attributes:
        redis: Redis client instance
        geo_reader: MaxMind GeoIP2 reader
    """
    
    def __init__(self, redis: Redis):
        self.redis = redis
        self.geo_reader = Reader('GeoLite2-City.mmdb')
    
    async def track_login(
        self,
        session_id: str,
        user_id: str,
        request: Request,
        success: bool
    ) -> None:
        """Track a login event.
        
        Args:
            session_id: Session ID
            user_id: User ID
            request: FastAPI request object
            success: Whether login was successful
        """
        # Parse user agent
        ua_string = request.headers.get("user-agent", "")
        user_agent = user_agents.parse(ua_string)
        
        # Get location data
        ip = request.client.host
        location = None
        try:
            location = self.geo_reader.city(ip)
        except:
            pass
        
        # Create login event
        event = LoginEvent(
            session_id=session_id,
            user_id=user_id,
            timestamp=datetime.utcnow(),
            ip_address=ip,
            user_agent=ua_string,
            device_type=user_agent.device.family,
            browser=user_agent.browser.family,
            os=user_agent.os.family,
            country=location.country.name if location else None,
            city=location.city.name if location else None,
            success=success
        )
        
        # Store event
        await self.redis.lpush(
            f"login_events:{user_id}",
            event.json()
        )
        
        # Update statistics
        pipe = self.redis.pipeline()
        
        # Increment total logins
        pipe.hincrby(f"user_stats:{user_id}", "total_logins", 1)
        
        # Increment success/failure count
        if success:
            pipe.hincrby(f"user_stats:{user_id}", "successful_logins", 1)
        else:
            pipe.hincrby(f"user_stats:{user_id}", "failed_logins", 1)
        
        # Update device stats
        pipe.hincrby(
            f"user_devices:{user_id}",
            event.device_type,
            1
        )
        
        # Update browser stats
        pipe.hincrby(
            f"user_browsers:{user_id}",
            event.browser,
            1
        )
        
        # Update location stats
        if event.country:
            pipe.hincrby(
                f"user_countries:{user_id}",
                event.country,
                1
            )
        
        await pipe.execute()
    
    async def track_security_event(
        self,
        event_type: str,
        session_id: str,
        user_id: str,
        request: Request,
        details: Dict
    ) -> None:
        """Track a security event.
        
        Args:
            event_type: Type of security event
            session_id: Session ID
            user_id: User ID
            request: FastAPI request object
            details: Event details
        """
        event = SecurityEvent(
            event_type=event_type,
            session_id=session_id,
            user_id=user_id,
            timestamp=datetime.utcnow(),
            ip_address=request.client.host,
            details=details
        )
        
        # Store event
        await self.redis.lpush(
            f"security_events:{user_id}",
            event.json()
        )
        
        # Update security stats
        await self.redis.hincrby(
            f"security_stats:{user_id}",
            event_type,
            1
        )
    
    async def get_user_stats(self, user_id: str) -> SessionStats:
        """Get session statistics for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            SessionStats: User session statistics
        """
        pipe = self.redis.pipeline()
        
        # Get basic stats
        pipe.hgetall(f"user_stats:{user_id}")
        pipe.hgetall(f"user_devices:{user_id}")
        pipe.hgetall(f"user_browsers:{user_id}")
        pipe.hgetall(f"user_countries:{user_id}")
        
        # Get active sessions
        pipe.scard(f"user_sessions:{user_id}")
        
        stats_data, devices, browsers, countries, active = await pipe.execute()
        
        # Calculate success rate
        total = int(stats_data.get("total_logins", 0))
        successful = int(stats_data.get("successful_logins", 0))
        success_rate = (successful / total) if total > 0 else 0
        
        # Calculate average session duration
        events = await self.redis.lrange(f"login_events:{user_id}", 0, -1)
        durations = []
        
        for i in range(len(events) - 1):
            current = LoginEvent.parse_raw(events[i])
            next_event = LoginEvent.parse_raw(events[i + 1])
            if current.success and next_event.success:
                duration = (next_event.timestamp - current.timestamp).total_seconds()
                durations.append(duration)
        
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        return SessionStats(
            total_sessions=total,
            active_sessions=active,
            devices={k: int(v) for k, v in devices.items()},
            browsers={k: int(v) for k, v in browsers.items()},
            countries={k: int(v) for k, v in countries.items()},
            average_session_duration=avg_duration,
            login_success_rate=success_rate
        )
    
    async def get_security_events(
        self,
        user_id: str,
        limit: int = 50
    ) -> List[SecurityEvent]:
        """Get recent security events for a user.
        
        Args:
            user_id: User ID
            limit: Maximum number of events to return
            
        Returns:
            List[SecurityEvent]: List of security events
        """
        events = await self.redis.lrange(
            f"security_events:{user_id}",
            0,
            limit - 1
        )
        
        return [SecurityEvent.parse_raw(event) for event in events]
    
    async def detect_anomalies(
        self,
        session_id: str,
        user_id: str,
        request: Request
    ) -> List[str]:
        """Detect suspicious session activity.
        
        Args:
            session_id: Session ID
            user_id: User ID
            request: FastAPI request object
            
        Returns:
            List[str]: List of detected anomalies
        """
        anomalies = []
        
        # Get user's normal patterns
        events = await self.redis.lrange(
            f"login_events:{user_id}",
            0,
            100
        )
        
        if not events:
            return anomalies
        
        # Analyze patterns
        locations = defaultdict(int)
        devices = defaultdict(int)
        browsers = defaultdict(int)
        
        for event_data in events:
            event = LoginEvent.parse_raw(event_data)
            if event.success:
                if event.country:
                    locations[event.country] += 1
                devices[event.device_type] += 1
                browsers[event.browser] += 1
        
        # Get current event data
        ua_string = request.headers.get("user-agent", "")
        user_agent = user_agents.parse(ua_string)
        
        try:
            location = self.geo_reader.city(request.client.host)
            country = location.country.name if location else None
        except:
            country = None
        
        # Check for anomalies
        if country and country not in locations:
            anomalies.append(f"Unusual login location: {country}")
        
        if user_agent.device.family not in devices:
            anomalies.append(f"Unusual device: {user_agent.device.family}")
        
        if user_agent.browser.family not in browsers:
            anomalies.append(f"Unusual browser: {user_agent.browser.family}")
        
        return anomalies 