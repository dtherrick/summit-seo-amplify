#!/usr/bin/env python3

import os
import sys
from typing import Dict, List, Optional
from dataclasses import dataclass
import re
from urllib.parse import urlparse
import argparse

@dataclass
class EnvVar:
    name: str
    required: bool = True
    validator: Optional[callable] = None
    description: str = ""
    required_in_build: bool = False

def validate_url(url: str) -> bool:
    """Validate if string is a proper URL."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_port(port: str) -> bool:
    """Validate port number."""
    try:
        port_num = int(port)
        return 1 <= port_num <= 65535
    except ValueError:
        return False

def validate_bool(value: str) -> bool:
    """Validate boolean string."""
    return value.lower() in ('true', 'false', '1', '0')

def validate_cors_origins(value: str) -> bool:
    """Validate CORS origins format."""
    try:
        # Strip brackets and split by comma
        origins = value.strip('[]').replace('"', '').split(',')
        return all(validate_url(origin.strip()) for origin in origins if origin.strip())
    except:
        return False

def validate_log_level(value: str) -> bool:
    """Validate log level case-insensitively."""
    valid_levels = ('debug', 'info', 'warning', 'error', 'critical')
    return value.lower() in valid_levels

# Define required environment variables and their validators
ENV_VARS: Dict[str, EnvVar] = {
    # Database
    'DATABASE_URL': EnvVar('DATABASE_URL', True, validate_url, 'PostgreSQL connection URL'),
    
    # Security
    'SECRET_KEY': EnvVar('SECRET_KEY', True, lambda x: len(x) >= 32, 'Secret key for JWT encoding'),
    'ACCESS_TOKEN_EXPIRE_MINUTES': EnvVar('ACCESS_TOKEN_EXPIRE_MINUTES', True, lambda x: x.isdigit(), 'JWT token expiration in minutes'),
    'REFRESH_TOKEN_EXPIRE_DAYS': EnvVar('REFRESH_TOKEN_EXPIRE_DAYS', True, lambda x: x.isdigit(), 'Refresh token expiration in days'),
    'SECURE_COOKIES': EnvVar('SECURE_COOKIES', True, validate_bool, 'Enable secure cookies'),
    
    # CORS and Security Headers
    'CORS_ORIGINS': EnvVar('CORS_ORIGINS', True, validate_cors_origins, 'Allowed CORS origins'),
    'SECURITY_HEADERS_ENABLED': EnvVar('SECURITY_HEADERS_ENABLED', True, validate_bool, 'Enable security headers'),
    
    # Redis
    'REDIS_URL': EnvVar('REDIS_URL', True, validate_url, 'Redis connection URL'),
    'REDIS_PASSWORD': EnvVar('REDIS_PASSWORD', True, lambda x: len(x) >= 16, 'Redis password'),
    
    # Email
    'SMTP_HOST': EnvVar('SMTP_HOST', True, None, 'SMTP server hostname'),
    'SMTP_PORT': EnvVar('SMTP_PORT', True, validate_port, 'SMTP server port'),
    'SMTP_USER': EnvVar('SMTP_USER', True, None, 'SMTP username'),
    'SMTP_PASSWORD': EnvVar('SMTP_PASSWORD', True, lambda x: len(x) >= 8, 'SMTP password'),
    'EMAIL_FROM': EnvVar('EMAIL_FROM', True, validate_email, 'Sender email address'),
    
    # Monitoring
    'LOG_LEVEL': EnvVar('LOG_LEVEL', True, validate_log_level, 'Logging level', True),
    'GRAFANA_ADMIN_PASSWORD': EnvVar('GRAFANA_ADMIN_PASSWORD', True, lambda x: len(x) >= 12, 'Grafana admin password'),
    
    # Infrastructure
    'PORT': EnvVar('PORT', True, validate_port, 'Application port', True),
    'WORKERS': EnvVar('WORKERS', True, lambda x: x.isdigit() and 1 <= int(x) <= 32, 'Number of worker processes', True),
    
    # Optional variables
    'SENTRY_DSN': EnvVar('SENTRY_DSN', False, validate_url, 'Sentry DSN for error tracking'),
    'AWS_ACCESS_KEY_ID': EnvVar('AWS_ACCESS_KEY_ID', False, None, 'AWS access key ID'),
    'AWS_SECRET_ACCESS_KEY': EnvVar('AWS_SECRET_ACCESS_KEY', False, None, 'AWS secret access key'),
}

def validate_environment(build_check: bool = False) -> List[str]:
    """
    Validate all environment variables.
    Args:
        build_check: If True, only validate variables required during build.
    Returns:
        List of error messages, empty if all validations pass.
    """
    errors = []
    
    for var_name, var_config in ENV_VARS.items():
        # Skip if we're doing a build check and this var isn't required during build
        if build_check and not var_config.required_in_build:
            continue
            
        value = os.getenv(var_name)
        
        # Check if required variable is missing
        if var_config.required and not value:
            errors.append(f"Required environment variable '{var_name}' is not set")
            continue
            
        # Skip validation for optional variables that are not set
        if not var_config.required and not value:
            continue
            
        # Validate value format if validator exists
        if value and var_config.validator and not var_config.validator(value):
            errors.append(f"Environment variable '{var_name}' has invalid format")
    
    return errors

def main():
    """Main function to run validation and exit with appropriate status code."""
    parser = argparse.ArgumentParser(description='Validate environment variables')
    parser.add_argument('--check-build', action='store_true', help='Only check variables required during build')
    parser.add_argument('--dev', action='store_true', help='Running in development mode')
    args = parser.parse_args()
    
    if args.dev:
        os.environ["NODE_ENV"] = "development"

    print("Validating environment variables...")
    errors = validate_environment(args.check_build)
    
    if errors:
        print("\nEnvironment validation failed!")
        print("The following errors were found:")
        for error in errors:
            print(f"❌ {error}")
        sys.exit(1)
    
    print("✅ Environment validation passed!")
    sys.exit(0)

if __name__ == "__main__":
    main()