"""empty message

Revision ID: 7abeb9f3ca17
Revises: 
Create Date: 2024-06-22 13:42:20.057201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7abeb9f3ca17'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=100),
               existing_nullable=False)
        batch_op.alter_column('author',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=50),
               existing_nullable=True)

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.alter_column('author',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=50),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.alter_column('author',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)

    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.alter_column('author',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)
        batch_op.alter_column('title',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=200),
               existing_nullable=False)

    # ### end Alembic commands ###