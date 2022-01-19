"""empty message

Revision ID: ff6127b7e211
Revises: effb0b0d6e97
Create Date: 2022-01-18 18:53:10.452421

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff6127b7e211'
down_revision = 'effb0b0d6e97'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contributed_asset', sa.Column('uuid', sa.Integer(), nullable=False))
    op.add_column('track_asset', sa.Column('uuid', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('track_asset', 'uuid')
    op.drop_column('contributed_asset', 'uuid')
    # ### end Alembic commands ###