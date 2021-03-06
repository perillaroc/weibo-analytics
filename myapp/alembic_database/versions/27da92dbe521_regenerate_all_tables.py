"""regenerate all tables

Revision ID: 27da92dbe521
Revises: None
Create Date: 2014-03-06 20:46:29.344000

"""

# revision identifiers, used by Alembic.
revision = '27da92dbe521'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('calendar',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('month', sa.Integer(), nullable=True),
    sa.Column('day', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('date')
    )
    op.create_table('weibo_list',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('uid', sa.BigInteger(), nullable=True),
    sa.Column('user_uid', sa.BigInteger(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('status_type', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.BigInteger(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('source', sa.Text(), nullable=True),
    sa.Column('original_pic', sa.Text(), nullable=True),
    sa.Column('bmiddle_pic', sa.Text(), nullable=True),
    sa.Column('thumbnail_pic', sa.Text(), nullable=True),
    sa.Column('geo', sa.Text(), nullable=True),
    sa.Column('retweeted_status', sa.Text(), nullable=True),
    sa.Column('reposts_count', sa.Integer(), nullable=True),
    sa.Column('comments_count', sa.Integer(), nullable=True),
    sa.Column('attitudes_count', sa.Integer(), nullable=True),
    sa.Column('visible_type', sa.Integer(), nullable=True),
    sa.Column('pic_urls', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('status_id'),
    sa.UniqueConstraint('uid')
    )
    op.create_table('user',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.Column('uid', sa.BigInteger(), nullable=True),
    sa.Column('info', sa.Text(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('last_login_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('token', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('uid')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles_users')
    op.drop_table('user')
    op.drop_table('weibo_list')
    op.drop_table('calendar')
    op.drop_table('role')
    ### end Alembic commands ###
