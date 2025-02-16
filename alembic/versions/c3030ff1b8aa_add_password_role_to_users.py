"""add password role to users

Revision ID: c3030ff1b8aa
Revises: b8dc298c4e65
Create Date: 2025-02-09 21:04:38.803964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3030ff1b8aa'
down_revision: Union[str, None] = 'b8dc298c4e65'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column("password", sa.String(250), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("users", "password")
