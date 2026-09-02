"""add tag icon

Revision ID: 1c6f2e8a4d3b
Revises: 7a3f0c9d2b41
Create Date: 2026-09-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c6f2e8a4d3b'
down_revision = '7a3f0c9d2b41'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('tag') as batch_op:
        batch_op.add_column(sa.Column('icon', sa.String(length=80), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('tag') as batch_op:
        batch_op.drop_column('icon')
