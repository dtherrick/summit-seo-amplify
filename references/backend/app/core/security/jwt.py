"""JWT token handling module.

This module provides functions for encoding and decoding JWT tokens
using the python-jose library.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from jose import JWTError, jwt
from pydantic import BaseModel

# TODO: Move these to settings
SECRET_KEY = "your-secret-key-here"  # Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class TokenPayload(BaseModel):
    """Token payload model."""
    sub: str
    exp: datetime
    type: str = "access"

def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create a new access token.
    
    Args:
        subject: Subject of the token (usually user ID)
        expires_delta: Optional expiration time delta

    Returns:
        str: Encoded JWT token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "type": "access"
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode and validate an access token.
    
    Args:
        token: JWT token to decode

    Returns:
        Optional[Dict[str, Any]]: Decoded token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            return None
        return payload
    except JWTError:
        return None 