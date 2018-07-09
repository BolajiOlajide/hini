"""empty message

Revision ID: 0c1923b4d32c
Revises: bfdd2aaa1d1b
Create Date: 2018-07-09 22:44:02.196744

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c1923b4d32c'
down_revision = 'bfdd2aaa1d1b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('state', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Users', 'state')
    # ### end Alembic commands ###