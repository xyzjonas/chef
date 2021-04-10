"""empty message

Revision ID: f91610b78d55
Revises: 3251a114750c
Create Date: 2021-04-10 11:41:22.149343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f91610b78d55'
down_revision = '3251a114750c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ingredient', sa.Column('fibers', sa.Float(), nullable=True))
    op.add_column('ingredient', sa.Column('proteins', sa.Float(), nullable=True))
    with op.batch_alter_table('ingredient') as batch_op:
        batch_op.drop_column('protein')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ingredient', sa.Column('protein', sa.FLOAT(), nullable=True))
    with op.batch_alter_table('ingredient') as batch_op:
        batch_op.drop_column('proteins')
        batch_op.drop_column('fibers')
    # ### end Alembic commands ###
