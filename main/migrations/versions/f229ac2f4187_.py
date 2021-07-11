"""empty message

Revision ID: f229ac2f4187
Revises: 
Create Date: 2021-07-10 19:07:18.288643

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f229ac2f4187'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('urls',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('long_url', sa.String(length=450), nullable=False),
    sa.Column('short_url', sa.String(length=10), nullable=False),
    sa.Column('times_visited', sa.Integer(), nullable=True),
    sa.Column('link_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('long_url'),
    sa.UniqueConstraint('short_url')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('urls')
    # ### end Alembic commands ###
