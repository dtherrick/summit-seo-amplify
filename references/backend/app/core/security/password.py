"""Password hashing and verification module.

This module provides functions for securely hashing and verifying passwords
using bcrypt through passlib.
"""

from passlib.context import CryptContext

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