"""add has_completed_survey column

Revision ID: 20240321_001
Revises: 20240319_001
Create Date: 2024-03-21 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20240321_001'
down_revision: Union[str, None] = '20240319_001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add has_completed_survey column to users table
    op.add_column('users', sa.Column('has_completed_survey', sa.Boolean(), nullable=False, server_default='false'))


def downgrade() -> None:
    # Remove has_completed_survey column from users table
    op.drop_column('users', 'has_completed_survey') 