"""empty message

Revision ID: 74a1aa5db0bb
Revises: 559ca127dba9
Create Date: 2021-12-03 15:15:48.575726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74a1aa5db0bb'
down_revision = '559ca127dba9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('asset_type', sa.Column('status', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('asset_type', 'status')
    # ### end Alembic commands ###
