"""Step-up authentication module.

This module provides additional authentication methods when
higher security is needed, including:
- TOTP (Time-based One-Time Password)
- Recovery codes
- Security questions
- Email verification
"""

from typing import Optional, List, Dict
from datetime import datetime, timedelta
import pyotp
import secrets
import json
from fastapi import HTTPException, status
from redis.asyncio import Redis
from pydantic import BaseModel

from app.core.config import get_settings
from app.core.mail import send_verification_email

settings = get_settings()

class StepUpMethod(BaseModel):
    """Step-up authentication method configuration."""
    type: str  # totp, recovery, questions, email
    enabled: bool
    data: Dict
    last_used: Optional[datetime]

class StepUpAuth:
    """Step-up authentication manager.
    
    Handles additional authentication methods when
    higher security is needed.
    """
    
    def __init__(self, redis: Redis):
        self.redis = redis
        self.verification_timeout = 300  # 5 minutes
    
    async def _get_key(self, type_: str, user_id: str) -> str:
        """Get Redis key for step-up data."""
        return f"step_up:{type_}:{user_id}"
    
    async def setup_totp(self, user_id: str) -> Dict:
        """Set up TOTP authentication.
        
        Args:
            user_id: User ID
            
        Returns:
            dict: TOTP setup data including secret and QR code
        """
        # Generate TOTP secret
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret)
        
        # Create provisioning URI for QR code
        uri = totp.provisioning_uri(
            name=user_id,
            issuer_name="Summit Agents"
        )
        
        # Store TOTP config
        method = StepUpMethod(
            type="totp",
            enabled=True,
            data={"secret": secret},
            last_used=None
        )
        
        await self.redis.hset(
            await self._get_key("methods", user_id),
            "totp",
            method.json()
        )
        
        return {
            "secret": secret,
            "uri": uri
        }
    
    async def verify_totp(self, user_id: str, code: str) -> bool:
        """Verify TOTP code.
        
        Args:
            user_id: User ID
            code: TOTP code
            
        Returns:
            bool: Whether code is valid
        """
        # Get TOTP config
        method_data = await self.redis.hget(
            await self._get_key("methods", user_id),
            "totp"
        )
        
        if not method_data:
            return False
        
        method = StepUpMethod.parse_raw(method_data)
        if not method.enabled:
            return False
        
        # Verify code
        totp = pyotp.TOTP(method.data["secret"])
        is_valid = totp.verify(code)
        
        if is_valid:
            # Update last used
            method.last_used = datetime.utcnow()
            await self.redis.hset(
                await self._get_key("methods", user_id),
                "totp",
                method.json()
            )
        
        return is_valid
    
    async def generate_recovery_codes(self, user_id: str) -> List[str]:
        """Generate recovery codes.
        
        Args:
            user_id: User ID
            
        Returns:
            List[str]: List of recovery codes
        """
        # Generate codes
        codes = [secrets.token_urlsafe(12) for _ in range(10)]
        
        # Store hashed codes
        method = StepUpMethod(
            type="recovery",
            enabled=True,
            data={"codes": codes},
            last_used=None
        )
        
        await self.redis.hset(
            await self._get_key("methods", user_id),
            "recovery",
            method.json()
        )
        
        return codes
    
    async def verify_recovery_code(self, user_id: str, code: str) -> bool:
        """Verify recovery code.
        
        Args:
            user_id: User ID
            code: Recovery code
            
        Returns:
            bool: Whether code is valid
        """
        # Get recovery codes
        method_data = await self.redis.hget(
            await self._get_key("methods", user_id),
            "recovery"
        )
        
        if not method_data:
            return False
        
        method = StepUpMethod.parse_raw(method_data)
        if not method.enabled:
            return False
        
        # Check code
        if code not in method.data["codes"]:
            return False
        
        # Remove used code
        method.data["codes"].remove(code)
        method.last_used = datetime.utcnow()
        
        # Update stored codes
        await self.redis.hset(
            await self._get_key("methods", user_id),
            "recovery",
            method.json()
        )
        
        return True
    
    async def setup_security_questions(
        self,
        user_id: str,
        questions: List[Dict[str, str]]
    ) -> None:
        """Set up security questions.
        
        Args:
            user_id: User ID
            questions: List of question/answer pairs
        """
        method = StepUpMethod(
            type="questions",
            enabled=True,
            data={"questions": questions},
            last_used=None
        )
        
        await self.redis.hset(
            await self._get_key("methods", user_id),
            "questions",
            method.json()
        )
    
    async def verify_security_questions(
        self,
        user_id: str,
        answers: List[str]
    ) -> bool:
        """Verify security question answers.
        
        Args:
            user_id: User ID
            answers: List of answers
            
        Returns:
            bool: Whether answers are correct
        """
        # Get questions
        method_data = await self.redis.hget(
            await self._get_key("methods", user_id),
            "questions"
        )
        
        if not method_data:
            return False
        
        method = StepUpMethod.parse_raw(method_data)
        if not method.enabled:
            return False
        
        # Check answers
        stored_answers = [q["answer"] for q in method.data["questions"]]
        if len(answers) != len(stored_answers):
            return False
        
        is_valid = all(
            a1.lower().strip() == a2.lower().strip()
            for a1, a2 in zip(answers, stored_answers)
        )
        
        if is_valid:
            method.last_used = datetime.utcnow()
            await self.redis.hset(
                await self._get_key("methods", user_id),
                "questions",
                method.json()
            )
        
        return is_valid
    
    async def send_verification_email(
        self,
        user_id: str,
        email: str
    ) -> None:
        """Send verification email.
        
        Args:
            user_id: User ID
            email: User's email address
        """
        # Generate verification code
        code = secrets.token_urlsafe(32)
        
        # Store code
        await self.redis.setex(
            await self._get_key("email", user_id),
            self.verification_timeout,
            code
        )
        
        # Send email
        await send_verification_email(email, code)
    
    async def verify_email_code(self, user_id: str, code: str) -> bool:
        """Verify email verification code.
        
        Args:
            user_id: User ID
            code: Verification code
            
        Returns:
            bool: Whether code is valid
        """
        stored_code = await self.redis.get(
            await self._get_key("email", user_id)
        )
        
        if not stored_code:
            return False
        
        return secrets.compare_digest(stored_code.decode(), code)
    
    async def get_available_methods(self, user_id: str) -> List[str]:
        """Get available step-up methods for user.
        
        Args:
            user_id: User ID
            
        Returns:
            List[str]: List of available methods
        """
        methods = await self.redis.hgetall(
            await self._get_key("methods", user_id)
        )
        
        return [
            method_type
            for method_type, method_data in methods.items()
            if StepUpMethod.parse_raw(method_data).enabled
        ] 