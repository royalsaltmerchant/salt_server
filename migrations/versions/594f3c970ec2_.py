"""empty message

Revision ID: 594f3c970ec2
Revises: c92bcc57203b
Create Date: 2022-05-19 15:04:42.947251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '594f3c970ec2'
down_revision = 'c92bcc57203b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('address', sa.String(length=120), nullable=True))
    op.add_column('user', sa.Column('phone', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'phone')
    op.drop_column('user', 'address')
    # ### end Alembic commands ###
