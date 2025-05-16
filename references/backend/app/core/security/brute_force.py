"""Brute force protection module.

This module provides protection against brute force attacks by:
- Tracking failed login attempts
- Implementing rate limiting
- Locking accounts after too many failures
"""

from typing import Optional
from datetime import datetime, timedelta
from redis.asyncio import Redis
from fastapi import HTTPException, status

from app.core.config import get_settings

settings = get_settings()

class BruteForceProtection:
    """Protection against brute force attacks.
    
    Tracks failed login attempts and implements rate limiting
    to prevent brute force attacks.
    """
    
    def __init__(self, redis: Redis):
        self.redis = redis
        self.max_attempts = 5  # Maximum failed attempts before lockout
        self.lockout_duration = 300  # Lockout duration in seconds (5 minutes)
        self.attempt_window = 300  # Window for counting attempts in seconds
    
    async def _get_key(self, identifier: str) -> str:
        """Get Redis key for brute force data."""
        return f"brute_force:{identifier}"
    
    async def check_attempts(self, identifier: str) -> None:
        """Check if too many failed attempts.
        
        Args:
            identifier: User identifier (email, username, etc.)
            
        Raises:
            HTTPException: If too many failed attempts
        """
        key = await self._get_key(identifier)
        
        # Get current attempts
        attempts = await self.redis.get(key)
        if not attempts:
            return
        
        attempts = int(attempts)
        if attempts >= self.max_attempts:
            # Check if still in lockout period
            ttl = await self.redis.ttl(key)
            if ttl > 0:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Too many failed attempts. Try again in {ttl} seconds."
                )
            else:
                # Reset attempts if lockout expired
                await self.redis.delete(key)
    
    async def record_failure(self, identifier: str) -> None:
        """Record a failed attempt.
        
        Args:
            identifier: User identifier (email, username, etc.)
        """
        key = await self._get_key(identifier)
        
        # Increment attempts
        attempts = await self.redis.incr(key)
        
        # Set expiry if first attempt
        if attempts == 1:
            await self.redis.expire(key, self.attempt_window)
    
    async def reset_attempts(self, identifier: str) -> None:
        """Reset failed attempts counter.
        
        Args:
            identifier: User identifier (email, username, etc.)
        """
        key = await self._get_key(identifier)
        await self.redis.delete(key)
    
    async def get_remaining_attempts(self, identifier: str) -> Optional[int]:
        """Get remaining allowed attempts.
        
        Args:
            identifier: User identifier (email, username, etc.)
            
        Returns:
            Optional[int]: Number of remaining attempts, or None if no attempts recorded
        """
        key = await self._get_key(identifier)
        attempts = await self.redis.get(key)
        
        if not attempts:
            return None
        
        attempts = int(attempts)
        return max(0, self.max_attempts - attempts)
    
    async def get_lockout_time(self, identifier: str) -> Optional[int]:
        """Get remaining lockout time in seconds.
        
        Args:
            identifier: User identifier (email, username, etc.)
            
        Returns:
            Optional[int]: Remaining lockout time in seconds, or None if not locked
        """
        key = await self._get_key(identifier)
        attempts = await self.redis.get(key)
        
        if not attempts or int(attempts) < self.max_attempts:
            return None
        
        return await self.redis.ttl(key)

    async def get_status(
        self,
        user_id: Optional[str],
        ip_address: str
    ) -> "BruteForceStatus":
        """Get brute force protection status.
        
        Args:
            user_id: Optional user ID
            ip_address: IP address
            
        Returns:
            BruteForceStatus: Status object containing protection info
        """
        # Check IP-based attempts
        ip_key = await self._get_key(ip_address)
        ip_attempts = await self.redis.get(ip_key)
        ip_attempts = int(ip_attempts) if ip_attempts else 0
        
        # Check user-based attempts if user_id provided
        user_attempts = 0
        if user_id:
            user_key = await self._get_key(user_id)
            user_attempts_data = await self.redis.get(user_key)
            user_attempts = int(user_attempts_data) if user_attempts_data else 0
        
        # Get total attempts
        total_attempts = max(ip_attempts, user_attempts)
        
        # Check if blocked
        is_blocked = total_attempts >= self.max_attempts
        
        # Get wait time if blocked
        wait_time = 0
        if is_blocked:
            if user_id:
                wait_time = await self.get_lockout_time(user_id) or 0
            if not wait_time:
                wait_time = await self.redis.ttl(ip_key)
        
        return BruteForceStatus(
            is_blocked=is_blocked,
            attempts=total_attempts,
            wait_time=wait_time
        )

class BruteForceStatus:
    """Status information for brute force protection."""
    
    def __init__(
        self,
        is_blocked: bool,
        attempts: int,
        wait_time: int
    ):
        self.is_blocked = is_blocked
        self.attempts = attempts
        self.wait_time = wait_time 