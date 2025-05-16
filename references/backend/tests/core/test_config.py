"""Tests for the configuration module.

This module contains tests for configuration loading,
validation, and environment variable handling.
"""

import os
import pytest
from pydantic import ValidationError
from typing import Any, Dict

from app.core.config import Settings, get_settings

@pytest.fixture
def env_vars() -> Dict[str, Any]:
    """Fixture for test environment variables."""
    return {
        "PROJECT_NAME": "Test Project",
        "VERSION": "0.1.0",
        "API_V1_STR": "/api/v1",
        "SECRET_KEY": "test_secret_key_123",
        "USER_MANAGER_SECRET": "test_user_manager_secret_123",
        "JWT_SECRET": "test_jwt_secret_123",
        "JWT_LIFETIME_SECONDS": "3600",
        "DATABASE_URL": "postgresql://user:pass@localhost:5432/testdb",
        "TEST_DATABASE_URL": "postgresql://user:pass@localhost:5432/test_testdb",
        "DB_ECHO": "false",
        "DB_POOL_SIZE": "5",
        "DB_MAX_OVERFLOW": "10",
        "RATE_LIMIT_TIMES": "60",
        "RATE_LIMIT_SECONDS": "60",
        "REDIS_URL": "redis://localhost:6379/0",
        "BACKEND_CORS_ORIGINS": '["http://localhost:3000"]',
        "LOG_LEVEL": "INFO",
        "SMTP_TLS": "true",
        "SMTP_PORT": "587",
        "SMTP_HOST": "smtp.example.com",
        "SMTP_USER": "test@example.com",
        "SMTP_PASSWORD": "testpass123",
        "EMAILS_FROM_EMAIL": "noreply@example.com",
        "EMAILS_FROM_NAME": "Test Project"
    }

@pytest.fixture
def mock_env(env_vars: Dict[str, Any], monkeypatch):
    """Set up mock environment variables."""
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    return env_vars

def test_settings_from_env(mock_env):
    """Test settings loaded from environment variables."""
    settings = get_settings()
    
    # Test basic settings
    assert settings.PROJECT_NAME == mock_env["PROJECT_NAME"]
    assert settings.VERSION == mock_env["VERSION"]
    assert settings.API_V1_STR == mock_env["API_V1_STR"]
    
    # Test security settings
    assert settings.SECRET_KEY == mock_env["SECRET_KEY"]
    assert settings.JWT_SECRET == mock_env["JWT_SECRET"]
    assert settings.JWT_LIFETIME_SECONDS == int(mock_env["JWT_LIFETIME_SECONDS"])
    
    # Test database settings
    assert settings.DATABASE_URL == mock_env["DATABASE_URL"]
    assert settings.DB_POOL_SIZE == int(mock_env["DB_POOL_SIZE"])
    assert settings.DB_MAX_OVERFLOW == int(mock_env["DB_MAX_OVERFLOW"])
    
    # Test rate limiting settings
    assert settings.RATE_LIMIT_TIMES == int(mock_env["RATE_LIMIT_TIMES"])
    assert settings.RATE_LIMIT_SECONDS == int(mock_env["RATE_LIMIT_SECONDS"])
    
    # Test Redis settings
    assert settings.REDIS_URL == mock_env["REDIS_URL"]
    
    # Test CORS settings
    assert settings.BACKEND_CORS_ORIGINS == ["http://localhost:3000"]
    
    # Test email settings
    assert settings.SMTP_TLS == (mock_env["SMTP_TLS"].lower() == "true")
    assert settings.SMTP_PORT == int(mock_env["SMTP_PORT"])
    assert settings.SMTP_HOST == mock_env["SMTP_HOST"]
    assert settings.SMTP_USER == mock_env["SMTP_USER"]
    assert settings.SMTP_PASSWORD == mock_env["SMTP_PASSWORD"]

def test_missing_required_settings(monkeypatch):
    """Test validation error on missing required settings."""
    # Clear all environment variables
    for var in os.environ:
        monkeypatch.delenv(var, raising=False)
    
    with pytest.raises(ValidationError):
        Settings()

def test_invalid_cors_origins(mock_env, monkeypatch):
    """Test validation of CORS origins format."""
    monkeypatch.setenv("BACKEND_CORS_ORIGINS", "invalid_json")
    
    with pytest.raises(ValidationError):
        Settings()

def test_invalid_database_url(mock_env, monkeypatch):
    """Test validation of database URL format."""
    monkeypatch.setenv("DATABASE_URL", "invalid_url")
    
    with pytest.raises(ValidationError):
        Settings()

def test_invalid_redis_url(mock_env, monkeypatch):
    """Test validation of Redis URL format."""
    monkeypatch.setenv("REDIS_URL", "invalid_url")
    
    with pytest.raises(ValidationError):
        Settings()

def test_invalid_email_settings(mock_env, monkeypatch):
    """Test validation of email settings."""
    monkeypatch.setenv("EMAILS_FROM_EMAIL", "invalid_email")
    
    with pytest.raises(ValidationError):
        Settings()

def test_settings_singleton():
    """Test that get_settings returns the same instance."""
    settings1 = get_settings()
    settings2 = get_settings()
    assert settings1 is settings2

def test_settings_immutable():
    """Test that settings are immutable after creation."""
    settings = get_settings()
    
    with pytest.raises(TypeError):
        settings.PROJECT_NAME = "New Name"

def test_default_values():
    """Test default values for optional settings."""
    settings = Settings(
        PROJECT_NAME="Test",
        SECRET_KEY="secret",
        DATABASE_URL="postgresql://user:pass@localhost:5432/testdb",
        REDIS_URL="redis://localhost:6379/0"
    )
    
    assert settings.LOG_LEVEL == "INFO"  # Default value
    assert settings.DB_ECHO is False  # Default value
    assert settings.JWT_ALGORITHM == "HS256"  # Default value 