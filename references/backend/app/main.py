"""Main FastAPI application module.

This module initializes and configures the FastAPI application,
including middleware, routers, and startup/shutdown events.
"""

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
import time
import logging

from app.core.config import get_settings
from app.core.middleware.security import SecurityMiddleware
from app.core.redis import init_redis_pool, close_redis_pool
from app.core.database import init_db, close_db
from app.core.metrics import setup_monitoring
from app.api import api_router

settings = get_settings()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Summit Agents API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Add security middleware
app.add_middleware(
    SecurityMiddleware,
    exclude_paths=[
        f"{settings.API_V1_STR}/docs",
        f"{settings.API_V1_STR}/redoc",
        f"{settings.API_V1_STR}/openapi.json",
        "/health",
        "/metrics"
    ]
)

# Add timing middleware
@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    """Add processing time header to response."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Include API router
app.include_router(api_router)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "app": "Summit Agents API",
        "version": "1.0.0",
        "docs_url": "/docs"
    }

# Set up Prometheus monitoring
setup_monitoring(app)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize connections on startup."""
    logger.info("Initializing application...")
    await init_redis_pool()
    await init_db()
    logger.info("Application initialized")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Close connections on shutdown."""
    logger.info("Shutting down application...")
    await close_redis_pool()
    await close_db()
    logger.info("Application shut down")