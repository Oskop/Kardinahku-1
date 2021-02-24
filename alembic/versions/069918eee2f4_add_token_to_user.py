"""add token to user

Revision ID: 069918eee2f4
Revises: c49b84181082
Create Date: 2021-02-23 19:24:30.783079

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '069918eee2f4'
down_revision = 'c49b84181082'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('token', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'token')
    # ### end Alembic commands ###