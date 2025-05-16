"""Prometheus metrics module.

This module configures Prometheus metrics collection for:
- Request latency
- Request counts
- Security events
- Device trust scores
- Authentication attempts
- Redis operations
- Database operations
"""

from prometheus_client import Counter, Histogram, Gauge
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from typing import Callable
from fastapi import FastAPI

# Request metrics
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "path", "status"]
)

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"]
)

# Security metrics
SECURITY_EVENTS = Counter(
    "security_events_total",
    "Total security events",
    ["event_type", "user_id"]
)

DEVICE_TRUST_SCORE = Gauge(
    "device_trust_score",
    "Device trust score",
    ["user_id", "device_id"]
)

AUTH_ATTEMPTS = Counter(
    "auth_attempts_total",
    "Total authentication attempts",
    ["success", "method", "user_id"]
)

# Redis metrics
REDIS_OPERATIONS = Counter(
    "redis_operations_total",
    "Total Redis operations",
    ["operation", "status"]
)

REDIS_LATENCY = Histogram(
    "redis_operation_duration_seconds",
    "Redis operation latency in seconds",
    ["operation"]
)

# Database metrics
DB_OPERATIONS = Counter(
    "db_operations_total",
    "Total database operations",
    ["operation", "status"]
)

DB_LATENCY = Histogram(
    "db_operation_duration_seconds",
    "Database operation latency in seconds",
    ["operation"]
)

# Custom metrics for business logic
BUSINESS_METRICS = Counter(
    "business_operations_total",
    "Total business operations",
    ["operation_type", "status"]
)

def track_security_event(event_type: str, user_id: str) -> None:
    """Track security event.
    
    Args:
        event_type: Type of security event
        user_id: User ID
    """
    SECURITY_EVENTS.labels(
        event_type=event_type,
        user_id=user_id
    ).inc()

def update_device_trust_score(
    user_id: str,
    device_id: str,
    score: float
) -> None:
    """Update device trust score.
    
    Args:
        user_id: User ID
        device_id: Device ID
        score: Trust score
    """
    DEVICE_TRUST_SCORE.labels(
        user_id=user_id,
        device_id=device_id
    ).set(score)

def track_auth_attempt(
    success: bool,
    method: str,
    user_id: str
) -> None:
    """Track authentication attempt.
    
    Args:
        success: Whether attempt was successful
        method: Authentication method used
        user_id: User ID
    """
    AUTH_ATTEMPTS.labels(
        success=str(success),
        method=method,
        user_id=user_id
    ).inc()

def track_redis_operation(
    operation: str,
    status: str = "success"
) -> None:
    """Track Redis operation.
    
    Args:
        operation: Operation type
        status: Operation status
    """
    REDIS_OPERATIONS.labels(
        operation=operation,
        status=status
    ).inc()

def track_db_operation(
    operation: str,
    status: str = "success"
) -> None:
    """Track database operation.
    
    Args:
        operation: Operation type
        status: Status of operation
    """
    DB_OPERATIONS.labels(
        operation=operation,
        status=status
    ).inc()

def track_business_operation(
    operation_type: str,
    status: str = "success"
) -> None:
    """Track business operation.
    
    Args:
        operation_type: Type of business operation
        status: Status of operation
    """
    BUSINESS_METRICS.labels(
        operation_type=operation_type,
        status=status
    ).inc()

def setup_monitoring(app: FastAPI) -> None:
    """Set up Prometheus monitoring for FastAPI app.
    
    Args:
        app: FastAPI application instance
    """
    # Initialize instrumentator
    instrumentator = Instrumentator()
    
    # Add default metrics
    instrumentator.add(
        metrics.request_size(
            should_include_handler=True,
            should_include_method=True,
            should_include_status=True
        )
    )
    
    instrumentator.add(
        metrics.response_size(
            should_include_handler=True,
            should_include_method=True,
            should_include_status=True
        )
    )
    
    instrumentator.add(
        metrics.latency(
            should_include_handler=True,
            should_include_method=True,
            should_include_status=True
        )
    )
    
    # Instrument app and expose metrics
    instrumentator.instrument(app).expose(app) 