from uuid import uuid4
from sqlalchemy import Column, String, Boolean, ForeignKey, Table, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ENUM
from .base import Base, TimestampMixin

# Role types
class RoleType(str):
    SUPERUSER = "superuser"
    BUSINESS_ADMIN = "business_admin"
    BUSINESS_USER = "business_user"

# Association table for user roles
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id')),
    Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id'))
)

class Business(Base, TimestampMixin):
    __tablename__ = 'businesses'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    customer_id = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    users = relationship("User", back_populates="business")

class User(Base, TimestampMixin):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    business_id = Column(UUID(as_uuid=True), ForeignKey('businesses.id'))
    has_completed_survey = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    business = relationship("Business", back_populates="users")
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    sessions = relationship("Session", back_populates="user")

class Role(Base, TimestampMixin):
    __tablename__ = 'roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    role = Column(SQLEnum('superuser', 'business_admin', 'business_user', name='roletype'), nullable=False)
    description = Column(String)
    
    # Relationships
    users = relationship("User", secondary=user_roles, back_populates="roles")

class Session(Base, TimestampMixin):
    __tablename__ = 'sessions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    token = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="sessions") 