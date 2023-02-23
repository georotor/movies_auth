"""empty message

Revision ID: 3988aa1d4594
Revises: 
Create Date: 2023-02-23 23:55:43.110435

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3988aa1d4594'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id')
    )
    op.create_table('user_history',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('action', sa.String(length=100), nullable=False),
    sa.Column('user_agent', sa.String(length=255), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('users_roles',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('role_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'role_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_roles')
    op.drop_table('user_history')
    op.drop_table('users')
    op.drop_table('roles')
    # ### end Alembic commands ###