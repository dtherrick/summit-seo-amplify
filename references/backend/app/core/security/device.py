"""Device fingerprinting and location-based security module.

This module provides device fingerprinting and location-based
security features, including:
- Device fingerprint generation and validation
- Location tracking and validation
- Device trust scoring
- Suspicious activity detection
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import hashlib
import json
from fastapi import Request
from redis.asyncio import Redis
from pydantic import BaseModel
import user_agents

from app.core.config import get_settings

settings = get_settings()

class DeviceInfo(BaseModel):
    """Device information model."""
    fingerprint: str
    user_agent: str
    ip_address: str
    location: Optional[Dict[str, str]]
    first_seen: datetime
    last_seen: datetime
    trust_score: float
    is_trusted: bool

class DeviceManager:
    """Device security manager.
    
    Handles device fingerprinting, location tracking,
    and suspicious activity detection.
    """
    
    def __init__(self, redis: Redis):
        self.redis = redis
        self.trust_threshold = 0.7
        self.location_weight = 0.4
        self.history_weight = 0.3
        self.pattern_weight = 0.3
        
    async def _get_key(self, type_: str, user_id: str) -> str:
        """Get Redis key for device data."""
        return f"device:{type_}:{user_id}"
    
    def _generate_fingerprint(self, request: Request) -> str:
        """Generate device fingerprint from request data.
        
        Args:
            request: FastAPI request object
            
        Returns:
            str: Device fingerprint hash
        """
        # Collect device data
        user_agent = request.headers.get("user-agent", "")
        ip = request.client.host
        accept = request.headers.get("accept", "")
        accept_language = request.headers.get("accept-language", "")
        accept_encoding = request.headers.get("accept-encoding", "")
        
        # Generate fingerprint
        fingerprint_data = f"{user_agent}|{ip}|{accept}|{accept_language}|{accept_encoding}"
        return hashlib.sha256(fingerprint_data.encode()).hexdigest()
    
    def _get_location(self, ip_address: str) -> Optional[Dict[str, str]]:
        """Get location data from IP address.
        
        Args:
            ip_address: IP address
            
        Returns:
            Optional[Dict[str, str]]: Location data if found
        """
        # For development, return a simple location based on IP
        if ip_address.startswith('127.') or ip_address == '::1':
            return {
                "country": "Local",
                "city": "Localhost",
                "latitude": "0",
                "longitude": "0"
            }
        return None
    
    def _calculate_location_score(
        self,
        current_location: Optional[Dict[str, str]],
        known_locations: List[Dict[str, str]]
    ) -> float:
        """Calculate location-based trust score.
        
        Args:
            current_location: Current location data
            known_locations: List of known locations
            
        Returns:
            float: Location trust score (0-1)
        """
        if not current_location or not known_locations:
            return 0.5
        
        # Check if location is known
        for known in known_locations:
            if (
                known["country"] == current_location["country"]
                and known["city"] == current_location["city"]
            ):
                return 1.0
        
        # If country matches but city differs
        for known in known_locations:
            if known["country"] == current_location["country"]:
                return 0.7
        
        return 0.3
    
    def _calculate_history_score(
        self,
        device_info: DeviceInfo,
        total_logins: int
    ) -> float:
        """Calculate history-based trust score.
        
        Args:
            device_info: Device information
            total_logins: Total number of logins
            
        Returns:
            float: History trust score (0-1)
        """
        # Consider device age
        age_days = (datetime.utcnow() - device_info.first_seen).days
        if age_days > 30:
            return 1.0
        
        # Consider login frequency
        if total_logins > 10:
            return 0.9
        elif total_logins > 5:
            return 0.7
        
        return 0.5
    
    def _calculate_pattern_score(
        self,
        request: Request,
        device_info: DeviceInfo
    ) -> float:
        """Calculate pattern-based trust score.
        
        Args:
            request: FastAPI request object
            device_info: Device information
            
        Returns:
            float: Pattern trust score (0-1)
        """
        current_ua = user_agents.parse(request.headers.get("user-agent", ""))
        stored_ua = user_agents.parse(device_info.user_agent)
        
        # Check if major attributes match
        if (
            current_ua.browser.family == stored_ua.browser.family
            and current_ua.os.family == stored_ua.os.family
            and current_ua.device.family == stored_ua.device.family
        ):
            return 1.0
        
        # If only browser version changed
        if (
            current_ua.browser.family == stored_ua.browser.family
            and current_ua.os.family == stored_ua.os.family
        ):
            return 0.8
        
        return 0.4
    
    async def process_device(
        self,
        request: Request,
        user_id: str
    ) -> DeviceInfo:
        """Process device information from request.
        
        Args:
            request: FastAPI request object
            user_id: User ID
            
        Returns:
            DeviceInfo: Processed device information
        """
        # Generate fingerprint
        fingerprint = self._generate_fingerprint(request)
        
        # Get existing device info
        device_key = await self._get_key("info", user_id)
        stored_data = await self.redis.hget(device_key, fingerprint)
        
        current_time = datetime.utcnow()
        location = self._get_location(request.client.host)
        
        if stored_data:
            # Update existing device info
            device_info = DeviceInfo.parse_raw(stored_data)
            device_info.last_seen = current_time
            
            # Update location history
            locations_key = await self._get_key("locations", user_id)
            known_locations = json.loads(
                await self.redis.get(locations_key) or "[]"
            )
            
            if location and location not in known_locations:
                known_locations.append(location)
                await self.redis.set(
                    locations_key,
                    json.dumps(known_locations)
                )
            
            # Calculate trust score
            total_logins = await self.redis.hincrby(
                await self._get_key("stats", user_id),
                "total_logins",
                1
            )
            
            location_score = self._calculate_location_score(
                location,
                known_locations
            )
            history_score = self._calculate_history_score(
                device_info,
                total_logins
            )
            pattern_score = self._calculate_pattern_score(
                request,
                device_info
            )
            
            device_info.trust_score = (
                location_score * self.location_weight
                + history_score * self.history_weight
                + pattern_score * self.pattern_weight
            )
            device_info.is_trusted = device_info.trust_score >= self.trust_threshold
            
        else:
            # Create new device info
            device_info = DeviceInfo(
                fingerprint=fingerprint,
                user_agent=request.headers.get("user-agent", ""),
                ip_address=request.client.host,
                location=location,
                first_seen=current_time,
                last_seen=current_time,
                trust_score=0.5,
                is_trusted=False
            )
            
            # Initialize location history
            if location:
                await self.redis.set(
                    await self._get_key("locations", user_id),
                    json.dumps([location])
                )
            
            # Initialize login stats
            await self.redis.hset(
                await self._get_key("stats", user_id),
                "total_logins",
                1
            )
        
        # Store updated device info
        await self.redis.hset(
            device_key,
            fingerprint,
            device_info.json()
        )
        
        return device_info
    
    async def get_device_info(
        self,
        user_id: str,
        fingerprint: str
    ) -> Optional[DeviceInfo]:
        """Get stored device information.
        
        Args:
            user_id: User ID
            fingerprint: Device fingerprint
            
        Returns:
            Optional[DeviceInfo]: Device information if found
        """
        stored_data = await self.redis.hget(
            await self._get_key("info", user_id),
            fingerprint
        )
        
        if stored_data:
            return DeviceInfo.parse_raw(stored_data)
        
        return None
    
    async def get_known_locations(
        self,
        user_id: str
    ) -> List[Dict[str, str]]:
        """Get known locations for user.
        
        Args:
            user_id: User ID
            
        Returns:
            List[Dict[str, str]]: List of known locations
        """
        locations = await self.redis.get(
            await self._get_key("locations", user_id)
        )
        
        if locations:
            return json.loads(locations)
        
        return []
    
    async def get_login_stats(self, user_id: str) -> Dict[str, int]:
        """Get login statistics for user.
        
        Args:
            user_id: User ID
            
        Returns:
            Dict[str, int]: Login statistics
        """
        stats = await self.redis.hgetall(
            await self._get_key("stats", user_id)
        )
        
        return {
            key: int(value)
            for key, value in stats.items()
        }
    
    async def mark_device_trusted(
        self,
        user_id: str,
        fingerprint: str
    ) -> None:
        """Mark device as trusted.
        
        Args:
            user_id: User ID
            fingerprint: Device fingerprint
        """
        device_info = await self.get_device_info(user_id, fingerprint)
        if device_info:
            device_info.is_trusted = True
            device_info.trust_score = 1.0
            
            await self.redis.hset(
                await self._get_key("info", user_id),
                fingerprint,
                device_info.json()
            )
    
    async def mark_device_untrusted(
        self,
        user_id: str,
        fingerprint: str
    ) -> None:
        """Mark device as untrusted.
        
        Args:
            user_id: User ID
            fingerprint: Device fingerprint
        """
        device_info = await self.get_device_info(user_id, fingerprint)
        if device_info:
            device_info.is_trusted = False
            device_info.trust_score = 0.0
            
            await self.redis.hset(
                await self._get_key("info", user_id),
                fingerprint,
                device_info.json()
            ) 