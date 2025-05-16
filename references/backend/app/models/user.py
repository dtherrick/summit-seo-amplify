"""User models for the application."""
from datetime import datetime
from typing import Optional
from uuid import UUID as PythonUUID, uuid4

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Table, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

# Association table for user roles
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", UUID, ForeignKey("users.id", ondelete="CASCADE")),
    Column("role_id", UUID, ForeignKey("roles.id", ondelete="CASCADE")),
)

class User(SQLAlchemyBaseUserTableUUID, Base):
    """User model that extends FastAPI Users base model."""
    
    __tablename__ = "users"

    # Override hashed_password from FastAPI Users to match our column name
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024),
        name="password_hash",  # This maps the hashed_password attribute to our password_hash column
        nullable=False,
    )

    # Required FastAPI Users fields
    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Additional fields beyond FastAPI Users base fields
    business_id: Mapped[Optional[PythonUUID]] = mapped_column(
        UUID,
        ForeignKey("businesses.id", ondelete="SET NULL"),
        nullable=True
    )
    has_completed_survey: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Relationships
    business = relationship("Business", back_populates="users")
    roles: Mapped[list["Role"]] = relationship(
        secondary=user_roles,
        back_populates="users",
        cascade="all, delete"
    )

class Business(Base):
    """Business model for multi-tenant support."""
    
    __tablename__ = "businesses"

    id: Mapped[PythonUUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid4
    )
    name: Mapped[str] = mapped_column(
        String(length=255),
        nullable=False
    )
    customer_id: Mapped[str] = mapped_column(
        String(length=255),
        unique=True,
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Relationships
    users: Mapped[list[User]] = relationship(
        back_populates="business",
        cascade="all, delete-orphan"
    )

class Role(Base):
    """Role model for user permissions."""
    
    __tablename__ = "roles"

    id: Mapped[PythonUUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid4
    )
    name: Mapped[str] = mapped_column(
        String(length=50),
        nullable=False,
        unique=True
    )
    description: Mapped[Optional[str]] = mapped_column(
        String(length=255),
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Relationships
    users: Mapped[list[User]] = relationship(
        secondary=user_roles,
        back_populates="roles"
    ) 