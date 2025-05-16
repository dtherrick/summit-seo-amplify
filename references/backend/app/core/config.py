"""Application configuration module.

This module manages the application's configuration using Pydantic settings management.
It provides a centralized location for all configuration values and ensures type safety
and validation for all settings.

The module supports configuration through environment variables and .env files, with
settings for:
- Project metadata
- Security configurations
- Database connections
- Redis settings
- Email configuration
- Rate limiting
- CORS settings

Example:
    ```python
    from app.core.config import get_settings

    settings = get_settings()
    database_url = settings.DATABASE_URL
    jwt_secret = settings.JWT_SECRET
    ```

Note:
    The settings are cached using lru_cache to prevent repeated environment variable
    reads. In testing environments, you may need to clear this cache if you're
    modifying environment variables during test execution.
"""
from functools import lru_cache
from typing import Any, Dict, Optional
from pathlib import Path
import sys

from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings management.
    
    This class uses Pydantic's BaseSettings to manage application configuration,
    supporting both environment variables and .env files. It includes validation
    and type conversion for all settings.

    Attributes:
        PROJECT_NAME: The name of the project
        VERSION: The current version of the application
        API_V1_STR: The API version prefix for all endpoints
        SECRET_KEY: The main application secret key
        USER_MANAGER_SECRET: Secret for user management operations
        JWT_SECRET: Secret for JWT token generation
        JWT_LIFETIME_SECONDS: Token lifetime in seconds
        BACKEND_CORS_ORIGINS: List of allowed CORS origins
        DATABASE_URL: PostgreSQL database connection URL
        DB_ECHO: Whether to echo SQL statements (for debugging)
        DB_POOL_SIZE: Database connection pool size
        DB_MAX_OVERFLOW: Maximum overflow connections
        REDIS_URL: Redis connection URL
        REDIS_MAX_CONNECTIONS: Maximum number of Redis connections in the pool
        LOG_LEVEL: Application logging level
        SMTP_TLS: Whether to use TLS for SMTP
        SMTP_PORT: SMTP server port
        SMTP_HOST: SMTP server host
        SMTP_USER: SMTP authentication username
        SMTP_PASSWORD: SMTP authentication password
        EMAILS_FROM_EMAIL: Default sender email address
        EMAILS_FROM_NAME: Default sender name
        EMAIL_VERIFICATION_EXPIRE_MINUTES: Email verification token expiration time in minutes
        PASSWORD_RESET_EXPIRE_MINUTES: Password reset token expiration time in minutes
        EMAIL_FROM: Default sender email address for email sending
        ENVIRONMENT: The environment the application is running in

    Example:
        ```python
        settings = Settings()
        print(settings.DATABASE_URL)
        print(settings.JWT_LIFETIME_SECONDS)
        ```
    """
    
    # Project metadata
    PROJECT_NAME: str = "Summit Agents"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"  # development, staging, production
    
    # Security
    SECRET_KEY: SecretStr
    USER_MANAGER_SECRET: str
    JWT_SECRET: str
    JWT_LIFETIME_SECONDS: int = 3600  # 1 hour
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    
    # Database
    DATABASE_URL: PostgresDsn
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    
    # Redis
    REDIS_URL: str = "redis://:password@redis:6379/0"
    REDIS_MAX_CONNECTIONS: int = 10
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Email
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None
    EMAIL_VERIFICATION_EXPIRE_MINUTES: int = 30
    PASSWORD_RESET_EXPIRE_MINUTES: int = 30
    EMAIL_FROM: Optional[str] = None
    
    # Model config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    
    @property
    def email_templates_dir(self) -> str:
        """Get the directory containing email templates.
        
        Returns:
            str: The absolute path to the email templates directory
        """
        return "app/email-templates/build"
    
    @property
    def async_database_url(self) -> str:
        """Get the async database URL for SQLAlchemy.
        
        This property converts the standard PostgreSQL URL to its async variant
        by replacing the protocol.
        
        Returns:
            str: The async database URL
        
        Example:
            ```python
            # If DATABASE_URL is "postgresql://user:pass@localhost/db"
            # This returns "postgresql+asyncpg://user:pass@localhost/db"
            ```
        """
        return str(self.DATABASE_URL).replace("postgresql://", "postgresql+asyncpg://")
    
    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        """Get FastAPI application configuration.
        
        This property returns a dictionary of kwargs used to configure the
        FastAPI application instance.
        
        Returns:
            Dict[str, Any]: Configuration dictionary for FastAPI
        
        Example:
            ```python
            from fastapi import FastAPI
            app = FastAPI(**settings.fastapi_kwargs)
            ```
        """
        return {
            "title": self.PROJECT_NAME,
            "version": self.VERSION,
            "openapi_url": f"{self.API_V1_STR}/openapi.json",
            "docs_url": f"{self.API_V1_STR}/docs",
            "redoc_url": f"{self.API_V1_STR}/redoc",
        }

@lru_cache
def get_settings() -> Settings:
    """Get a cached instance of the application settings.
    
    This function uses lru_cache to cache the settings instance, preventing
    repeated reads of environment variables.
    
    Returns:
        Settings: The application settings instance
    
    Note:
        In testing environments, you may need to clear the lru_cache if you're
        modifying environment variables during test execution.
    """
    return Settings()

def find_templates_directory():
    current_dir = Path.cwd()
    
    # Check if 'templates' exists in current directory
    if (current_dir / "templates").is_dir():
        return current_dir / "templates"
    
    # Check one level deep
    for item in current_dir.iterdir():
        if item.is_dir() and (item / "templates").is_dir():
            return item / "templates"
    
    # Check two levels deep
    for item in current_dir.iterdir():
        if item.is_dir():
            for subitem in item.iterdir():
                if subitem.is_dir() and (subitem / "templates").is_dir():
                    return subitem / "templates"
    
    # If not found
    return None