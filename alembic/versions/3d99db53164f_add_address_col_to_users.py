"""add address col to users

Revision ID: 3d99db53164f
Revises: c3030ff1b8aa
Create Date: 2025-02-09 21:23:10.911298

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d99db53164f'
down_revision: Union[str, None] = 'c3030ff1b8aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('test')
    op.add_column('users', sa.Column('address', sa.String(), nullable=True))
    # Set a default value
    op.execute("UPDATE users SET address = 'default_address'")
    op.alter_column('users', 'address', nullable=False)
    op.execute("ALTER TABLE users ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE USING created_at::timestamp with time zone;")

    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_unique_constraint(None, 'users', ['email'])
    op.drop_column('users', 'password')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.VARCHAR(
        length=250), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.alter_column('users', 'created_at',
                    existing_type=sa.DateTime(timezone=True),
                    type_=sa.VARCHAR(),
                    nullable=False)
    op.drop_column('users', 'address')
    op.create_table('test',
                    sa.Column('id', sa.INTEGER(),
                              autoincrement=True, nullable=False),
                    sa.Column('num', sa.INTEGER(),
                              autoincrement=False, nullable=True),
                    sa.Column('data', sa.TEXT(),
                              autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('id', name='test_pkey')
                    )
    # ### end Alembic commands ###
