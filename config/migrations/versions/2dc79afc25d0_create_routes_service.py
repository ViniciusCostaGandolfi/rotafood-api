"""create routes service

Revision ID: 2dc79afc25d0
Revises: d9d9aa5544ae
Create Date: 2024-01-10 08:55:50.569079

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2dc79afc25d0'
down_revision: Union[str, None] = 'd9d9aa5544ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('routes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('total_distance', sa.Float(), nullable=True),
    sa.Column('total_volume', sa.Float(), nullable=True),
    sa.Column('link_google_maps', sa.String(), nullable=True),
    sa.Column('sequence', sa.ARRAY(sa.Integer()), nullable=True),
    sa.Column('merchant_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['merchant_id'], ['merchants.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('route_orders',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('index', sa.Integer(), nullable=True),
    sa.Column('route_id', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['route_id'], ['routes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('order_deliveries', 'index')
    op.add_column('orders', sa.Column('total_volume', sa.Float(), nullable=True))
    op.add_column('orders', sa.Column('total_price', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'total_price')
    op.drop_column('orders', 'total_volume')
    op.add_column('order_deliveries', sa.Column('index', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_table('route_orders')
    op.drop_table('routes')
    # ### end Alembic commands ###
