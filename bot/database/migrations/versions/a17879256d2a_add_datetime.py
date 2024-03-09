"""add_datetime

Revision ID: a17879256d2a
Revises: f0552ebc178d
Create Date: 2024-03-09 18:47:49.751633

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a17879256d2a'
down_revision: Union[str, None] = 'f0552ebc178d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('updated_by', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'updated_by')
    # ### end Alembic commands ###
