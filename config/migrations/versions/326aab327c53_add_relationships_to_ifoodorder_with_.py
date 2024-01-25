"""add relationships to IFoodOrder with Order

Revision ID: 326aab327c53
Revises: 63d0f24b0e59
Create Date: 2024-01-15 16:45:56.044477

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '326aab327c53'
down_revision: Union[str, None] = '63d0f24b0e59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ifood_orders', sa.Column('order_from_ifood_id', sa.String(), nullable=False))
    op.drop_column('ifood_orders', 'ifood_order_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ifood_orders', sa.Column('ifood_order_id', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('ifood_orders', 'order_from_ifood_id')
    # ### end Alembic commands ###
