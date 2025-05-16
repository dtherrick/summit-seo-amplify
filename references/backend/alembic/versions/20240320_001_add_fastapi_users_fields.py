"""Add FastAPI Users fields

Revision ID: 20240320_001
Revises: 20240319_001
Create Date: 2024-03-20 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20240320_001'
down_revision = '20240319_001'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add FastAPI Users required fields
    op.add_column('users', sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='false'))

def downgrade() -> None:
    # Remove FastAPI Users fields
    op.drop_column('users', 'is_superuser')
    op.drop_column('users', 'is_verified') 