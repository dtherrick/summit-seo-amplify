"""Configuration settings for the application."""
import os
from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    """Application settings."""

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Summit SEO Amplify"

    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["*"]  # In production, restrict to specific frontend domains

    # AWS settings
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")

    # Cognito settings
    COGNITO_USER_POOL_ID: Optional[str] = os.getenv("COGNITO_USER_POOL_ID")
    COGNITO_APP_CLIENT_ID: Optional[str] = os.getenv("COGNITO_APP_CLIENT_ID")
    COGNITO_DOMAIN: Optional[str] = os.getenv("COGNITO_DOMAIN")

    # DynamoDB settings
    DYNAMODB_USERS_TABLE: str = os.getenv("DYNAMODB_USERS_TABLE", "SummitSEOAmplify-Users")
    DYNAMODB_TENANTS_TABLE: str = os.getenv("DYNAMODB_TENANTS_TABLE", "SummitSEOAmplify-Tenants")

    class Config:
        """Pydantic config."""
        case_sensitive = True
        env_file = ".env"

# Create global settings object
settings = Settings()