"""Exception handling module.

This module defines custom exceptions for the application, providing a consistent
way to handle and report errors across the API. Each exception maps to a specific
HTTP status code and includes appropriate error details.

The module provides a hierarchy of exceptions:
- BusinessException: Base exception for all business logic errors
- NotFoundException: For resource not found errors (404)
- UnauthorizedException: For authentication failures (401)
- ForbiddenException: For authorization failures (403)
- ValidationException: For data validation errors (422)
- ConflictException: For resource conflicts (409)

Example:
    ```python
    from fastapi import FastAPI
    from app.core.exceptions import NotFoundException

    app = FastAPI()

    @app.get("/items/{item_id}")
    async def get_item(item_id: str):
        if not item_exists(item_id):
            raise NotFoundException("Item", item_id)
        return get_item_by_id(item_id)
    ```

Note:
    All exceptions in this module inherit from FastAPI's HTTPException,
    ensuring proper handling in the FastAPI framework.
"""
from typing import Any, Dict, Optional

from fastapi import HTTPException, status

class BusinessException(HTTPException):
    """Base exception for business logic errors.
    
    This is the base exception class for all business-specific exceptions
    in the application. It extends FastAPI's HTTPException to ensure proper
    handling in the framework.

    Attributes:
        status_code: The HTTP status code to return
        detail: A human-readable error message
        headers: Optional HTTP headers to include in the response

    Example:
        ```python
        raise BusinessException(
            status_code=400,
            detail="Invalid business operation",
            headers={"X-Error-Code": "INVALID_OPERATION"}
        )
        ```
    """
    
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the exception.
        
        Args:
            status_code: The HTTP status code to return
            detail: A human-readable error message
            headers: Optional HTTP headers to include in the response
        """
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class NotFoundException(BusinessException):
    """Exception for resource not found errors.
    
    This exception should be raised when a requested resource cannot be found
    in the system. It automatically sets the status code to 404.

    Attributes:
        resource: The type of resource that was not found
        resource_id: The ID of the resource that was not found

    Example:
        ```python
        raise NotFoundException("User", "123e4567-e89b-12d3-a456-426614174000")
        ```
    """
    
    def __init__(self, resource: str, resource_id: str) -> None:
        """Initialize the exception.
        
        Args:
            resource: The type of resource that was not found
            resource_id: The ID of the resource that was not found
        """
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} with id {resource_id} not found",
        )

class UnauthorizedException(BusinessException):
    """Exception for unauthorized access.
    
    This exception should be raised when authentication fails or is missing.
    It automatically sets the status code to 401 and includes the
    WWW-Authenticate header.

    Example:
        ```python
        raise UnauthorizedException("Invalid credentials")
        ```
    """
    
    def __init__(self, detail: str = "Unauthorized") -> None:
        """Initialize the exception.
        
        Args:
            detail: A human-readable error message
        """
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

class ForbiddenException(BusinessException):
    """Exception for forbidden access.
    
    This exception should be raised when an authenticated user attempts to
    access a resource they don't have permission for. It automatically sets
    the status code to 403.

    Example:
        ```python
        raise ForbiddenException("Insufficient permissions to access this resource")
        ```
    """
    
    def __init__(self, detail: str = "Forbidden") -> None:
        """Initialize the exception.
        
        Args:
            detail: A human-readable error message
        """
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )

class ValidationException(BusinessException):
    """Exception for validation errors.
    
    This exception should be raised when input data fails validation rules.
    It automatically sets the status code to 422.

    Example:
        ```python
        raise ValidationException("Email address is not in a valid format")
        ```
    """
    
    def __init__(self, detail: str) -> None:
        """Initialize the exception.
        
        Args:
            detail: A human-readable error message describing the validation failure
        """
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
        )

class ConflictException(BusinessException):
    """Exception for conflict errors.
    
    This exception should be raised when a resource conflict occurs, such as
    attempting to create a resource that already exists. It automatically sets
    the status code to 409.

    Example:
        ```python
        raise ConflictException("A user with this email already exists")
        ```
    """
    
    def __init__(self, detail: str) -> None:
        """Initialize the exception.
        
        Args:
            detail: A human-readable error message describing the conflict
        """
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        ) 