"""add performance indexes to posts

Revision ID: 9b1234567890
Revises: c7c37e6b1b59
Create Date: 2025-11-26 17:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b1234567890'
down_revision: Union[str, Sequence[str], None] = 'c7c37e6b1b59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create index on user_id for faster filtering by user
    op.create_index(op.f('ix_posts_user_id'), 'posts', ['user_id'], unique=False)
    
    # Create index on created_at for sorting feeds
    op.create_index(op.f('ix_posts_created_at'), 'posts', ['created_at'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_posts_created_at'), table_name='posts')
    op.drop_index(op.f('ix_posts_user_id'), table_name='posts')
