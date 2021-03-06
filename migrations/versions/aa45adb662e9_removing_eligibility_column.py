"""removing eligibility column

Revision ID: aa45adb662e9
Revises: f7caaf4b7614
Create Date: 2021-08-30 17:30:40.916888

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa45adb662e9'
down_revision = 'f7caaf4b7614'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'eligible')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('eligible', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
