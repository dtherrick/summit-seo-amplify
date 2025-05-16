"""Admin router for session analytics and monitoring.

This module provides admin endpoints for:
- Session statistics and analytics
- Security event monitoring
- User session management
- Anomaly detection
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Request, Query
from datetime import datetime, timedelta

from app.core.analytics.session import SessionAnalytics, SessionStats, SecurityEvent
from app.core.auth import get_current_admin
from app.core.redis import get_redis
from app.models.user import User

router = APIRouter()

@router.get("/stats/{user_id}", response_model=SessionStats)
async def get_user_session_stats(
    user_id: str,
    request: Request,
    admin: User = Depends(get_current_admin)
):
    """Get session statistics for a user.
    
    Args:
        user_id: User ID to get stats for
        request: Request object
        admin: Current admin user
        
    Returns:
        SessionStats: User session statistics
    """
    redis = await get_redis()
    analytics = SessionAnalytics(redis)
    return await analytics.get_user_stats(user_id)

@router.get("/security/{user_id}", response_model=List[SecurityEvent])
async def get_user_security_events(
    user_id: str,
    request: Request,
    limit: int = Query(50, gt=0, le=100),
    admin: User = Depends(get_current_admin)
):
    """Get security events for a user.
    
    Args:
        user_id: User ID to get events for
        request: Request object
        limit: Maximum number of events to return
        admin: Current admin user
        
    Returns:
        List[SecurityEvent]: List of security events
    """
    redis = await get_redis()
    analytics = SessionAnalytics(redis)
    return await analytics.get_security_events(user_id, limit)

@router.get("/anomalies/{user_id}")
async def check_session_anomalies(
    user_id: str,
    session_id: str,
    request: Request,
    admin: User = Depends(get_current_admin)
):
    """Check for session anomalies.
    
    Args:
        user_id: User ID to check
        session_id: Session ID to check
        request: Request object
        admin: Current admin user
        
    Returns:
        dict: Detected anomalies
    """
    redis = await get_redis()
    analytics = SessionAnalytics(redis)
    anomalies = await analytics.detect_anomalies(
        session_id,
        user_id,
        request
    )
    
    return {
        "user_id": user_id,
        "session_id": session_id,
        "anomalies": anomalies,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/active")
async def get_active_sessions(
    request: Request,
    admin: User = Depends(get_current_admin)
):
    """Get all active sessions.
    
    Args:
        request: Request object
        admin: Current admin user
        
    Returns:
        dict: Active session statistics
    """
    redis = await get_redis()
    
    # Get all user session keys
    cursor = 0
    user_keys = []
    
    while True:
        cursor, keys = await redis.scan(
            cursor,
            match="user_sessions:*",
            count=100
        )
        user_keys.extend(keys)
        if cursor == 0:
            break
    
    # Get active sessions for each user
    total_active = 0
    user_sessions = {}
    
    for key in user_keys:
        user_id = key.decode().split(":")[1]
        count = await redis.scard(key)
        if count > 0:
            user_sessions[user_id] = count
            total_active += count
    
    return {
        "total_active_sessions": total_active,
        "users_with_sessions": len(user_sessions),
        "session_distribution": user_sessions,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/summary")
async def get_session_summary(
    request: Request,
    timeframe: str = Query(
        "24h",
        regex="^(1h|24h|7d|30d)$"
    ),
    admin: User = Depends(get_current_admin)
):
    """Get session statistics summary.
    
    Args:
        request: Request object
        timeframe: Time period to summarize (1h, 24h, 7d, 30d)
        admin: Current admin user
        
    Returns:
        dict: Session statistics summary
    """
    redis = await get_redis()
    analytics = SessionAnalytics(redis)
    
    # Calculate time range
    now = datetime.utcnow()
    if timeframe == "1h":
        start_time = now - timedelta(hours=1)
    elif timeframe == "24h":
        start_time = now - timedelta(days=1)
    elif timeframe == "7d":
        start_time = now - timedelta(days=7)
    else:  # 30d
        start_time = now - timedelta(days=30)
    
    # Get all user keys
    cursor = 0
    user_keys = []
    
    while True:
        cursor, keys = await redis.scan(
            cursor,
            match="login_events:*",
            count=100
        )
        user_keys.extend(keys)
        if cursor == 0:
            break
    
    # Aggregate statistics
    total_logins = 0
    successful_logins = 0
    failed_logins = 0
    unique_users = set()
    unique_ips = set()
    devices = defaultdict(int)
    browsers = defaultdict(int)
    countries = defaultdict(int)
    
    for key in user_keys:
        events = await redis.lrange(key, 0, -1)
        user_id = key.decode().split(":")[1]
        
        for event_data in events:
            event = LoginEvent.parse_raw(event_data)
            if event.timestamp < start_time:
                continue
            
            total_logins += 1
            unique_users.add(event.user_id)
            unique_ips.add(event.ip_address)
            
            if event.success:
                successful_logins += 1
            else:
                failed_logins += 1
            
            devices[event.device_type] += 1
            browsers[event.browser] += 1
            if event.country:
                countries[event.country] += 1
    
    return {
        "timeframe": timeframe,
        "total_logins": total_logins,
        "successful_logins": successful_logins,
        "failed_logins": failed_logins,
        "unique_users": len(unique_users),
        "unique_ips": len(unique_ips),
        "success_rate": (successful_logins / total_logins) if total_logins > 0 else 0,
        "device_distribution": dict(devices),
        "browser_distribution": dict(browsers),
        "country_distribution": dict(countries),
        "timestamp": now.isoformat()
    } 