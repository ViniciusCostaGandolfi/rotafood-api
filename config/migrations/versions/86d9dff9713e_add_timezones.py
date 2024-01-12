"""add timezones

Revision ID: 86d9dff9713e
Revises: 8fed8ecb2ce7
Create Date: 2024-01-10 16:31:09.279961

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '86d9dff9713e'
down_revision: Union[str, None] = '8fed8ecb2ce7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum('IMMEDIATE', 'SCHEDULED', name='ordertimming').create(op.get_bind())
    op.add_column('orders', sa.Column('order_timing', postgresql.ENUM('IMMEDIATE', 'SCHEDULED', name='ordertimming', create_type=False), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'order_timing')
    sa.Enum('IMMEDIATE', 'SCHEDULED', name='ordertimming').drop(op.get_bind())
    # ### end Alembic commands ###
