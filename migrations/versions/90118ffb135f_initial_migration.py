"""Initial migration

Revision ID: 90118ffb135f
Revises: 
Create Date: 2024-06-12 17:25:28.105796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90118ffb135f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('feature', schema=None) as batch_op:
        batch_op.add_column(sa.Column('feature_code', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('value', sa.String(length=255), nullable=False))

    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.alter_column('shorten_url',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.alter_column('shorten_url',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)

    with op.batch_alter_table('feature', schema=None) as batch_op:
        batch_op.drop_column('value')
        batch_op.drop_column('feature_code')

    # ### end Alembic commands ###
