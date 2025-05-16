"""Input validation and sanitization module.

This module provides utilities for validating and sanitizing input data,
ensuring data integrity and security across the application.

The module includes:
- Input validation rules
- Data sanitization utilities
- Schema validation
- Common validation patterns

Example:
    ```python
    from app.core.validation import (
        validate_input,
        sanitize_html,
        validate_email
    )
    
    # Validate user input
    errors = validate_input(user_data, UserSchema)
    
    # Sanitize HTML content
    safe_content = sanitize_html(user_content)
    ```
"""

from typing import Any, Dict, List, Optional, Type, Union
import re
import html
from pydantic import BaseModel, ValidationError
from email_validator import validate_email as validate_email_format, EmailNotValidError
import bleach
from urllib.parse import urlparse
import json

# Allowed HTML tags and attributes for rich text
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 'ol', 'ul', 'li',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a'
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target'],
    '*': ['class']
}

def validate_input(data: Dict[str, Any], schema: Type[BaseModel]) -> List[str]:
    """Validate input data against a Pydantic schema.
    
    Args:
        data: Input data to validate
        schema: Pydantic model class to validate against
        
    Returns:
        List[str]: List of validation errors
        
    Example:
        ```python
        errors = validate_input(user_data, UserCreateSchema)
        if errors:
            raise HTTPException(
                status_code=422,
                detail={"errors": errors}
            )
        ```
    """
    try:
        schema(**data)
        return []
    except ValidationError as e:
        return [error["msg"] for error in e.errors()]

def sanitize_html(content: str) -> str:
    """Sanitize HTML content to prevent XSS attacks.
    
    Args:
        content: HTML content to sanitize
        
    Returns:
        str: Sanitized HTML content
        
    Example:
        ```python
        safe_content = sanitize_html(user_submitted_html)
        ```
    """
    return bleach.clean(
        content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )

def validate_email(email: str) -> tuple[bool, Optional[str]]:
    """Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        tuple[bool, Optional[str]]: (is_valid, error_message)
        
    Example:
        ```python
        is_valid, error = validate_email(user_email)
        if not is_valid:
            raise HTTPException(
                status_code=422,
                detail=error
            )
        ```
    """
    try:
        validate_email_format(email)
        return True, None
    except EmailNotValidError as e:
        return False, str(e)

def sanitize_string(value: str) -> str:
    """Sanitize a string by escaping HTML characters.
    
    Args:
        value: String to sanitize
        
    Returns:
        str: Sanitized string
        
    Example:
        ```python
        safe_text = sanitize_string(user_input)
        ```
    """
    return html.escape(value.strip())

def validate_url(url: str) -> tuple[bool, Optional[str]]:
    """Validate URL format and scheme.
    
    Args:
        url: URL to validate
        
    Returns:
        tuple[bool, Optional[str]]: (is_valid, error_message)
        
    Example:
        ```python
        is_valid, error = validate_url(website_url)
        if not is_valid:
            raise HTTPException(
                status_code=422,
                detail=error
            )
        ```
    """
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False, "Invalid URL format"
        if result.scheme not in ["http", "https"]:
            return False, "URL must use HTTP or HTTPS"
        return True, None
    except Exception:
        return False, "Invalid URL"

def sanitize_json(value: str) -> tuple[bool, Union[Dict, List, str]]:
    """Sanitize and validate JSON data.
    
    Args:
        value: JSON string to sanitize
        
    Returns:
        tuple[bool, Union[Dict, List, str]]: (is_valid, result/error)
        
    Example:
        ```python
        is_valid, result = sanitize_json(json_data)
        if not is_valid:
            raise HTTPException(
                status_code=422,
                detail=result
            )
        ```
    """
    try:
        # Parse JSON
        data = json.loads(value)
        
        # Recursively sanitize strings in JSON
        def sanitize_dict(obj: Any) -> Any:
            if isinstance(obj, dict):
                return {k: sanitize_dict(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [sanitize_dict(item) for item in obj]
            elif isinstance(obj, str):
                return sanitize_string(obj)
            return obj
        
        return True, sanitize_dict(data)
    except json.JSONDecodeError:
        return False, "Invalid JSON format"
    except Exception as e:
        return False, str(e)

def validate_phone_number(phone: str) -> tuple[bool, Optional[str]]:
    """Validate phone number format.
    
    Args:
        phone: Phone number to validate
        
    Returns:
        tuple[bool, Optional[str]]: (is_valid, error_message)
        
    Example:
        ```python
        is_valid, error = validate_phone_number(user_phone)
        if not is_valid:
            raise HTTPException(
                status_code=422,
                detail=error
            )
        ```
    """
    # Remove any non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Check length (assuming international format)
    if len(digits) < 10 or len(digits) > 15:
        return False, "Phone number must be between 10 and 15 digits"
    
    return True, None

class ValidationRules:
    """Common validation rules and patterns.
    
    This class provides static methods for common validation patterns
    used across the application.
    """
    
    @staticmethod
    def username(value: str) -> tuple[bool, Optional[str]]:
        """Validate username format.
        
        Args:
            value: Username to validate
            
        Returns:
            tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        if len(value) < 3:
            return False, "Username must be at least 3 characters"
        if len(value) > 30:
            return False, "Username must be at most 30 characters"
        if not re.match(r'^[a-zA-Z0-9_-]+$', value):
            return False, "Username can only contain letters, numbers, underscores, and hyphens"
        return True, None
    
    @staticmethod
    def business_name(value: str) -> tuple[bool, Optional[str]]:
        """Validate business name format.
        
        Args:
            value: Business name to validate
            
        Returns:
            tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        if len(value) < 2:
            return False, "Business name must be at least 2 characters"
        if len(value) > 100:
            return False, "Business name must be at most 100 characters"
        return True, None
    
    @staticmethod
    def description(value: str) -> tuple[bool, Optional[str]]:
        """Validate description text.
        
        Args:
            value: Description to validate
            
        Returns:
            tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        if len(value) > 1000:
            return False, "Description must be at most 1000 characters"
        return True, None 