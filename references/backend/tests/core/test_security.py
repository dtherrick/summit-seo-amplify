"""Tests for the security module.

This module contains tests for password hashing, JWT token
generation and validation, and other security-related functions.
"""

import pytest
from datetime import datetime, timedelta
from jose import jwt, JWTError

from app.core.security import (
    create_jwt_token,
    verify_jwt_token,
    get_password_hash,
    verify_password
)
from app.core.config import settings

pytestmark = pytest.mark.asyncio

def test_password_hashing():
    """Test password hashing and verification."""
    password = "testpass123"
    hashed = get_password_hash(password)
    
    # Verify hashed password is different from original
    assert hashed != password
    
    # Verify password verification works
    assert verify_password(password, hashed)
    
    # Verify wrong password fails
    assert not verify_password("wrongpass", hashed)

def test_create_jwt_token():
    """Test JWT token creation."""
    data = {"sub": "test@example.com"}
    token = create_jwt_token(data)
    
    # Decode token and verify claims
    payload = jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM]
    )
    
    assert payload["sub"] == data["sub"]
    assert "exp" in payload
    assert "iat" in payload

def test_create_jwt_token_with_expire():
    """Test JWT token creation with custom expiration."""
    data = {"sub": "test@example.com"}
    expire_delta = timedelta(minutes=15)
    token = create_jwt_token(data, expires_delta=expire_delta)
    
    # Decode token and verify expiration
    payload = jwt.decode(
        token,
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM]
    )
    
    exp_time = datetime.fromtimestamp(payload["exp"])
    iat_time = datetime.fromtimestamp(payload["iat"])
    assert (exp_time - iat_time) == expire_delta

def test_verify_jwt_token():
    """Test JWT token verification."""
    original_data = {"sub": "test@example.com"}
    token = create_jwt_token(original_data)
    
    # Verify token and check data
    payload = verify_jwt_token(token)
    assert payload["sub"] == original_data["sub"]

def test_verify_expired_token():
    """Test verification of expired JWT token."""
    data = {"sub": "test@example.com"}
    expire_delta = timedelta(microseconds=1)  # Expire immediately
    token = create_jwt_token(data, expires_delta=expire_delta)
    
    # Wait for token to expire
    import time
    time.sleep(0.1)
    
    # Verify token raises error
    with pytest.raises(JWTError):
        verify_jwt_token(token)

def test_verify_invalid_token():
    """Test verification of invalid JWT token."""
    invalid_token = "invalid.token.here"
    
    with pytest.raises(JWTError):
        verify_jwt_token(invalid_token)

def test_verify_tampered_token():
    """Test verification of tampered JWT token."""
    data = {"sub": "test@example.com"}
    token = create_jwt_token(data)
    
    # Tamper with the token
    parts = token.split(".")
    parts[1] = parts[1][:-1] + "X"  # Change last character
    tampered_token = ".".join(parts)
    
    with pytest.raises(JWTError):
        verify_jwt_token(tampered_token)

def test_password_hashing_different_salts():
    """Test that same password hashes differently."""
    password = "testpass123"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)
    
    # Verify hashes are different due to salt
    assert hash1 != hash2
    
    # Verify both hashes work for verification
    assert verify_password(password, hash1)
    assert verify_password(password, hash2)

def test_password_verification_timing():
    """Test that password verification timing is consistent."""
    import time
    
    password = "testpass123"
    wrong_password = "wrongpass123"
    hashed = get_password_hash(password)
    
    # Time correct password verification
    start = time.perf_counter()
    verify_password(password, hashed)
    correct_time = time.perf_counter() - start
    
    # Time wrong password verification
    start = time.perf_counter()
    verify_password(wrong_password, hashed)
    wrong_time = time.perf_counter() - start
    
    # Verify timing difference is minimal (within 2x)
    # This helps prevent timing attacks
    assert abs(correct_time - wrong_time) < correct_time 