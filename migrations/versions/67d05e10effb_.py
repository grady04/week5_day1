"""empty message

Revision ID: 67d05e10effb
Revises: 9cd14787da77
Create Date: 2022-06-15 13:42:55.610105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67d05e10effb'
down_revision = '9cd14787da77'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pokemon',
    sa.Column('pokemon_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('base_exp', sa.Integer(), nullable=True),
    sa.Column('sprite', sa.String(), nullable=True),
    sa.Column('ability', sa.String(), nullable=True),
    sa.Column('hp', sa.Integer(), nullable=True),
    sa.Column('attack', sa.Integer(), nullable=True),
    sa.Column('defense', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('pokemon_id')
    )
    op.create_table('poke_team',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('poke_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['poke_id'], ['pokemon.pokemon_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('user', sa.Column('wins', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('losses', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'losses')
    op.drop_column('user', 'wins')
    op.drop_table('poke_team')
    op.drop_table('pokemon')
    # ### end Alembic commands ###
