"""API router module."""
from fastapi import APIRouter

# Import routers from other API modules
from .users import router as users_router
from .tenants import router as tenants_router
# Uncomment and modify as new route modules are created
# from .auth import router as auth_router
# from .analysis import router as analysis_router

# Create main API router
api_router = APIRouter()

# Include routers
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(tenants_router, prefix="/tenants", tags=["tenants"])
# api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
# api_router.include_router(analysis_router, prefix="/analysis", tags=["analysis"])