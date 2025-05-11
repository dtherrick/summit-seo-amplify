"""API router module."""
from fastapi import APIRouter

# Import routers from other API modules
# from .users import router as old_users_router # Assuming this was for other user ops
from .tenants import router as tenants_router
from .endpoints.users import router as user_profile_router # New router for /users/me
# Uncomment and modify as new route modules are created
# from .auth import router as auth_router
# from .analysis import router as analysis_router

# Create main API router
api_router = APIRouter()

# Include routers
api_router.include_router(user_profile_router, prefix="/users", tags=["User Profile"])
api_router.include_router(tenants_router, prefix="/tenants", tags=["tenants"])
# api_router.include_router(old_users_router, prefix="/admin/users", tags=["Admin Users"]) # Example if you have other user routes
# api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
# api_router.include_router(analysis_router, prefix="/analysis", tags=["analysis"])