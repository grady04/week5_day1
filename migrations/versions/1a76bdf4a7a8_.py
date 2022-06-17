"""empty message

Revision ID: 1a76bdf4a7a8
Revises: 1a42b4bd1e86
Create Date: 2022-06-16 20:43:35.809671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a76bdf4a7a8'
down_revision = '1a42b4bd1e86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('favorite', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'favorite')
    # ### end Alembic commands ###
