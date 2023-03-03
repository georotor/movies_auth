"""empty message

Revision ID: 8980c9edc3f5
Revises: 80c1c19e165b
Create Date: 2023-03-01 22:45:55.942188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8980c9edc3f5'
down_revision = '80c1c19e165b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('social_account', schema=None) as batch_op:
        batch_op.create_unique_constraint('social_user', ['user_id', 'social_name'])
        batch_op.create_unique_constraint(None, ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('social_account', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint('social_user', type_='unique')

    # ### end Alembic commands ###
