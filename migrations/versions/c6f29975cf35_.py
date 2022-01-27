"""empty message

Revision ID: c6f29975cf35
Revises: f09fb367b65a
Create Date: 2022-01-26 09:46:37.206603

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6f29975cf35'
down_revision = 'f09fb367b65a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'about')
    # ### end Alembic commands ###