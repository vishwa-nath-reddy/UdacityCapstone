"""empty message

Revision ID: b5ffeeb1ecbc
Revises: 
Create Date: 2023-05-08 20:37:11.054038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5ffeeb1ecbc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Movie',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('language', sa.String(), nullable=False),
    sa.Column('producer', sa.String(), nullable=False),
    sa.Column('director', sa.String(), nullable=False),
    sa.Column('budget', sa.Integer(), nullable=False),
    sa.Column('actors', sa.String(), nullable=False),
    sa.Column('planned_release_date', sa.DateTime(), nullable=False),
    sa.Column('ticket_price', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Venue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('city', sa.String(length=120), nullable=False),
    sa.Column('state', sa.String(length=120), nullable=False),
    sa.Column('address', sa.String(length=120), nullable=False),
    sa.Column('capacity', sa.Integer(), nullable=False),
    sa.Column('contact_number', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Show',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('movie_charge', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['movie_id'], ['Movie.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Show')
    op.drop_table('Venue')
    op.drop_table('Movie')
    # ### end Alembic commands ###
