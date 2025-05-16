"""create auth tables

Revision ID: 20240319_001
Create Date: 2024-03-19 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base

# revision identifiers, used by Alembic.
revision = '20240319_001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Drop existing roletype enum if it exists
    op.execute("DROP TYPE IF EXISTS roletype")
    
    # Create role_type enum
    op.execute("CREATE TYPE roletype AS ENUM ('superuser', 'business_admin', 'business_user')")
    
    # Create businesses table
    op.create_table(
        'businesses',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('customer_id', sa.String(), unique=True, nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()'))
    )
    
    # Create roles table
    op.create_table(
        'roles',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('role', postgresql.ENUM('superuser', 'business_admin', 'business_user', name='roletype', create_type=False), nullable=False),
        sa.Column('description', sa.String()),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()'))
    )
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('business_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('businesses.id')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()'))
    )
    
    # Create user_roles association table
    op.create_table(
        'user_roles',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('role_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('roles.id'), primary_key=True)
    )
    
    # Create sessions table
    op.create_table(
        'sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('token', sa.String(), unique=True, nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()'))
    )
    
    # Create indexes
    op.create_index('ix_users_email', 'users', ['email'])
    op.create_index('ix_businesses_customer_id', 'businesses', ['customer_id'])
    op.create_index('ix_sessions_token', 'sessions', ['token'])
    
    # Insert default roles
    op.execute("""
        INSERT INTO roles (id, role, description)
        VALUES 
        (gen_random_uuid(), 'superuser', 'Super administrator with full access'),
        (gen_random_uuid(), 'business_admin', 'Business administrator'),
        (gen_random_uuid(), 'business_user', 'Regular business user')
    """)

def downgrade() -> None:
    # Drop tables
    op.drop_table('sessions')
    op.drop_table('user_roles')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('businesses')
    
    # Drop enum type
    op.execute('DROP TYPE roletype') 