"""Security utilities module.

This module provides security-related functionality for the application,
including password hashing, JWT token management, and ID generation utilities.
It uses industry-standard libraries for cryptographic operations:
- passlib with bcrypt for password hashing
- python-jose for JWT token handling

The module provides:
- Password hashing and verification
- JWT token creation and validation
- Utility functions for generating secure IDs

Example:
    ```python
    from app.core.security import verify_password, create_access_token

    # Password verification
    is_valid = verify_password("plain_password", hashed_password)

    # Token creation
    token = create_access_token({"sub": "user@example.com"})
    ```

Note:
    Ensure that SECRET_KEY is properly set in production environment.
    Never use the default development key in production.
"""
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from uuid import UUID
import os

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")  # Change in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash.
    
    Uses bcrypt to verify the password hash. This is a timing-safe operation.

    Args:
        plain_password: The password in plain text
        hashed_password: The hashed password to verify against

    Returns:
        bool: True if the password matches, False otherwise

    Example:
        ```python
        is_valid = verify_password("user_password", stored_hash)
        if is_valid:
            print("Password is correct")
        ```
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate a secure hash of a password.
    
    Uses bcrypt to generate a secure hash with salt.

    Args:
        password: The password to hash

    Returns:
        str: The hashed password with salt

    Example:
        ```python
        hashed = get_password_hash("user_password")
        # Store hashed password in database
        ```
    """
    return pwd_context.hash(password)

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT access token.
    
    Generates a JWT token with the provided data and expiration time.

    Args:
        data: Dictionary containing data to encode in the token
        expires_delta: Optional custom expiration time delta

    Returns:
        str: The encoded JWT token

    Example:
        ```python
        token = create_access_token(
            data={"sub": "user@example.com"},
            expires_delta=timedelta(hours=1)
        )
        ```

    Note:
        If no expiration delta is provided, uses ACCESS_TOKEN_EXPIRE_MINUTES
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """Decode and verify a JWT access token.
    
    Decodes the token and verifies its signature and expiration.

    Args:
        token: The JWT token to decode

    Returns:
        Optional[dict]: The decoded payload if valid, None if invalid

    Example:
        ```python
        payload = decode_access_token(token)
        if payload:
            user_id = payload.get("sub")
        ```

    Note:
        Returns None if the token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

class SecurityUtils:
    """Utility class for security-related operations.
    
    This class provides static utility methods for various security
    operations like ID generation.
    """

    @staticmethod
    def generate_customer_id(business_name: str) -> str:
        """Generate a unique customer ID for a business.
        
        Creates a unique identifier combining business name prefix
        and timestamp.

        Args:
            business_name: The name of the business

        Returns:
            str: A unique customer ID in format "PRE-YYYYMMDDHHMMSS"

        Example:
            ```python
            id = SecurityUtils.generate_customer_id("Acme Corp")
            # Returns something like "ACM-20240322123456"
            ```

        Note:
            The ID uses the first 3 letters of the business name
            (uppercase) as a prefix
        """
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        # Take first 3 letters of business name, uppercase them, and remove spaces
        prefix = ''.join(business_name.split())[0:3].upper()
        return f"{prefix}-{timestamp}" 