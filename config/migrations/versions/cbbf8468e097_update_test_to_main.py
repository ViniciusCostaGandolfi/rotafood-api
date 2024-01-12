"""update test to main

Revision ID: cbbf8468e097
Revises: 28e7f33fd0e1
Create Date: 2024-01-12 14:16:29.220492

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cbbf8468e097'
down_revision: Union[str, None] = '28e7f33fd0e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum('OWNER', 'ADM', 'GARSON', 'CHEF', 'DRIVER', name='role').drop(op.get_bind())
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum('OWNER', 'ADM', 'GARSON', 'CHEF', 'DRIVER', name='role').create(op.get_bind())
    # ### end Alembic commands ###
