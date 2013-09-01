"""add token in user

Revision ID: 3582dc71cce4
Revises: 1784593c102f
Create Date: 2013-09-01 20:32:23.305000

"""

# revision identifiers, used by Alembic.
revision = '3582dc71cce4'
down_revision = '1784593c102f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('token', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'token')
    ### end Alembic commands ###