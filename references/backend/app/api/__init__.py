"""API package.

This package contains all API endpoints organized by version.
"""

from fastapi import APIRouter
from .v1 import auth_router, business_router, surveys_router

# Create main API router
api_router = APIRouter()

# Include v1 routes
api_router.include_router(auth_router, prefix="/v1/auth", tags=["auth"])
api_router.include_router(business_router, prefix="/v1/business", tags=["business"])
api_router.include_router(surveys_router, prefix="/v1/surveys", tags=["surveys"])

__all__ = ["api_router"]
