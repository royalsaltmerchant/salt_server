"""empty message

Revision ID: 911a850ef87d
Revises: c8e993154640
Create Date: 2021-12-21 18:17:28.723466

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '911a850ef87d'
down_revision = 'c8e993154640'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('track_asset', 'metadata',
               existing_type=postgresql.ARRAY(postgresql.DOUBLE_PRECISION(precision=53)),
               type_=sa.ARRAY(sa.String()),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('track_asset', 'metadata',
               existing_type=sa.ARRAY(sa.String()),
               type_=postgresql.ARRAY(postgresql.DOUBLE_PRECISION(precision=53)),
               existing_nullable=True)
    # ### end Alembic commands ###
