"""Email functionality module.

This module provides email-related functionality including:
- Email verification
- Password reset
- Security notifications
"""

from typing import List, Optional
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from app.core.config import get_settings, find_templates_directory

settings = get_settings()

# Get the absolute path to the templates directory
TEMPLATE_DIR = find_templates_directory()

# Configure email settings
conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.EMAIL_FROM,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False,
    TEMPLATE_FOLDER=TEMPLATE_DIR
)

async def send_verification_email(
    email: EmailStr,
    verification_code: str,
    username: Optional[str] = None
) -> None:
    """Send verification email to user.
    
    Args:
        email: User's email address
        verification_code: Verification code
        username: Optional username for personalization
    """
    message = MessageSchema(
        subject="Verify your email address",
        recipients=[email],
        template_body={
            "username": username or "there",
            "verification_code": verification_code,
            "expiry_minutes": settings.EMAIL_VERIFICATION_EXPIRE_MINUTES
        },
        subtype="html"
    )
    
    fm = FastMail(conf)
    await fm.send_message(message, template_name="verification_email.html")

async def send_password_reset_email(
    email: EmailStr,
    reset_token: str,
    username: Optional[str] = None
) -> None:
    """Send password reset email to user.
    
    Args:
        email: User's email address
        reset_token: Password reset token
        username: Optional username for personalization
    """
    message = MessageSchema(
        subject="Reset your password",
        recipients=[email],
        template_body={
            "username": username or "there",
            "reset_token": reset_token,
            "expiry_minutes": settings.PASSWORD_RESET_EXPIRE_MINUTES
        },
        subtype="html"
    )
    
    fm = FastMail(conf)
    await fm.send_message(message, template_name="password_reset_email.html")

async def send_security_alert_email(
    email: EmailStr,
    alert_type: str,
    details: dict,
    username: Optional[str] = None
) -> None:
    """Send security alert email to user.
    
    Args:
        email: User's email address
        alert_type: Type of security alert
        details: Alert details
        username: Optional username for personalization
    """
    message = MessageSchema(
        subject=f"Security Alert: {alert_type}",
        recipients=[email],
        template_body={
            "username": username or "there",
            "alert_type": alert_type,
            "details": details
        },
        subtype="html"
    )
    
    fm = FastMail(conf)
    await fm.send_message(message, template_name="security_alert_email.html") 