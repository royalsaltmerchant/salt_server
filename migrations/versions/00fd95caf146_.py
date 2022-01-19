"""empty message

Revision ID: 00fd95caf146
Revises: ff6127b7e211
Create Date: 2022-01-18 19:14:26.603332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00fd95caf146'
down_revision = 'ff6127b7e211'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contributed_asset', 'uuid',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=False)
    op.alter_column('track_asset', 'uuid',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('track_asset', 'uuid',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('contributed_asset', 'uuid',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    # ### end Alembic commands ###
