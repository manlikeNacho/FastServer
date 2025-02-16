from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e25a98f3c296'
down_revision = '472349b02bf8'
branch_labels = None
depends_on = None


def upgrade():
    # Add the password column with a default value
    op.add_column('users', sa.Column('password', sa.String(),
                  nullable=False, server_default='default_password'))
    # Remove the server_default after setting the default value
    op.alter_column('users', 'password', server_default=None)


def downgrade():
    op.drop_column('users', 'password')
