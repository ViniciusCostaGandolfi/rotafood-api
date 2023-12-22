"""create table order_item_options 

Revision ID: 424b293cf56a
Revises: 2c78f5a34be6
Create Date: 2023-12-13 09:54:41.584586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '424b293cf56a'
down_revision: Union[str, None] = '2c78f5a34be6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order_item_options',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('order_item_id', sa.Integer(), nullable=True),
    sa.Column('product_option_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_item_id'], ['order_items.id'], ),
    sa.ForeignKeyConstraint(['product_option_id'], ['product_options.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_item_options')
    # ### end Alembic commands ###
