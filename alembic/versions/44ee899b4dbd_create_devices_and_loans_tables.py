"""create devices and loans tables

Revision ID: 44ee899b4dbd
Revises: 8e03120735cb
Create Date: 2026-06-18 19:54:25.841440
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '44ee899b4dbd'
down_revision: Union[str, Sequence[str], None] = '8e03120735cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass