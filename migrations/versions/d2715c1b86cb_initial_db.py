"""initial_db

Revision ID: d2715c1b86cb
Revises: 
Create Date: 2024-06-26 19:54:00.833390

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd2715c1b86cb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('addresses',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('street_name', sa.String(length=64), nullable=True),
    sa.Column('formatted_address', sa.String(length=64), nullable=False),
    sa.Column('street_number', sa.String(length=64), nullable=False),
    sa.Column('city', sa.String(length=64), nullable=False),
    sa.Column('postal_code', sa.String(length=64), nullable=False),
    sa.Column('neighborhood', sa.String(length=64), nullable=False),
    sa.Column('state', sa.String(length=64), nullable=False),
    sa.Column('complement', sa.String(length=64), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cvrps',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('secconds_to_solve', sa.DECIMAL(precision=10, scale=3), nullable=True),
    sa.Column('total_discente_meters', sa.DECIMAL(precision=10, scale=3), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_takeouts',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('mode', sa.String(length=32), nullable=True),
    sa.Column('takeout_date_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('prices',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('value', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('original_value', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('merchants',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('corporate_name', sa.String(length=64), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=False),
    sa.Column('document_type', sa.String(length=4), nullable=False),
    sa.Column('document', sa.String(length=16), nullable=False),
    sa.Column('merchant_type', sa.String(length=12), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('address_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['addresses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('routes',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('total_volume_liters', sa.DECIMAL(precision=10, scale=3), nullable=False),
    sa.Column('total_weight_grams', sa.DECIMAL(precision=10, scale=3), nullable=False),
    sa.Column('toal_items_quantity', sa.Integer(), nullable=False),
    sa.Column('total_distance_meters', sa.DECIMAL(precision=10, scale=3), nullable=False),
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.Column('cvrp_out_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['cvrp_out_id'], ['cvrps.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('scale_prices',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('min_quantity', sa.Integer(), nullable=False),
    sa.Column('price_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['price_id'], ['prices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('catalogs',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.Column('catalog_context_modifier', sa.String(length=32), nullable=False),
    sa.Column('merchant_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['merchant_id'], ['merchants.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('categories',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('status', sa.String(length=16), nullable=False),
    sa.Column('index', sa.Integer(), nullable=False),
    sa.Column('template', sa.String(length=16), nullable=False),
    sa.Column('merchant_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['merchant_id'], ['merchants.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('merchant_users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('phone', sa.String(length=255), nullable=True),
    sa.Column('permissions', postgresql.ARRAY(sa.String(length=64)), nullable=True),
    sa.Column('merchant_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['merchant_id'], ['merchants.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('orders',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('order_type', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('preparation_start_date_time', sa.DateTime(), nullable=True),
    sa.Column('sales_channel', sa.String(), nullable=True),
    sa.Column('order_timing', sa.String(), nullable=True),
    sa.Column('extra_info', sa.String(), nullable=True),
    sa.Column('merchant_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['merchant_id'], ['merchants.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('description', sa.String(length=1024), nullable=False),
    sa.Column('ean', sa.String(length=256), nullable=False),
    sa.Column('additional_information', sa.String(length=1024), nullable=False),
    sa.Column('product_type', sa.String(length=32), nullable=False),
    sa.Column('dietary_restrictions', postgresql.ARRAY(sa.String(length=32)), nullable=True),
    sa.Column('weight_unit', sa.String(length=8), nullable=False),
    sa.Column('weight', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('volume_unit', sa.String(length=8), nullable=False),
    sa.Column('volume', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('merchant_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['merchant_id'], ['merchants.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vehicles',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('km_per_liter', sa.DECIMAL(precision=10, scale=3), nullable=True),
    sa.Column('max_volume_liters', sa.DECIMAL(precision=10, scale=3), nullable=True),
    sa.Column('max_weight_grams', sa.DECIMAL(precision=10, scale=3), nullable=True),
    sa.Column('max_items_quantity', sa.Integer(), nullable=True),
    sa.Column('max_distance_meters', sa.DECIMAL(precision=10, scale=3), nullable=True),
    sa.Column('cvrp_in_id', sa.UUID(), nullable=True),
    sa.Column('route_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['cvrp_in_id'], ['cvrps.id'], ),
    sa.ForeignKeyConstraint(['route_id'], ['routes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('catalog_categories',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('catalog_id', sa.UUID(), nullable=True),
    sa.Column('category_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['catalog_id'], ['catalogs.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('items',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('type', sa.String(length=64), nullable=False),
    sa.Column('status', sa.String(length=16), nullable=False),
    sa.Column('index', sa.Integer(), nullable=False),
    sa.Column('dietary_restrictions', postgresql.ARRAY(sa.String(length=32)), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('product_id', sa.UUID(), nullable=True),
    sa.Column('price_id', sa.UUID(), nullable=True),
    sa.Column('category_id', sa.UUID(), nullable=True),
    sa.Column('merchant_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['merchant_id'], ['merchants.id'], ),
    sa.ForeignKeyConstraint(['price_id'], ['prices.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('option_groups',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('external_code', sa.String(), nullable=True),
    sa.Column('index', sa.Integer(), nullable=True),
    sa.Column('option_group_type', sa.String(), nullable=True),
    sa.Column('product_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_additional_fees',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('type', sa.String(length=255), nullable=False),
    sa.Column('value', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('full_description', sa.Text(), nullable=True),
    sa.Column('order_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_benefits',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('description', sa.String(length=32), nullable=True),
    sa.Column('value', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('target', sa.String(length=32), nullable=True),
    sa.Column('order_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_customers',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('document_number', sa.String(), nullable=True),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('segmentation', sa.String(), nullable=True),
    sa.Column('orders_count_on_merchant', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_deliveries',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('mode', sa.String(), nullable=True),
    sa.Column('pickup_code', sa.String(), nullable=True),
    sa.Column('delivered_by', sa.String(), nullable=True),
    sa.Column('delivery_address_id', sa.UUID(), nullable=True),
    sa.Column('delivery_date_time', sa.DateTime(), nullable=True),
    sa.Column('address_id', sa.UUID(), nullable=True),
    sa.Column('order_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['addresses.id'], ),
    sa.ForeignKeyConstraint(['delivery_address_id'], ['addresses.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_indoors',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('mode', sa.String(length=32), nullable=True),
    sa.Column('delivery_date_time', sa.DateTime(), nullable=True),
    sa.Column('order_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_payments',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('method', sa.String(), nullable=True),
    sa.Column('prepaid', sa.Boolean(), nullable=True),
    sa.Column('currency', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('value', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('order_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_schedules',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('delivery_date_time_start', sa.DateTime(), nullable=True),
    sa.Column('delivery_date_time_end', sa.DateTime(), nullable=True),
    sa.Column('order_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_totals',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('benefits', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('delivery_fee', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('order_amount', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('sub_total', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('additional_fees', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('order_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('route_orders',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('route_id', sa.UUID(), nullable=True),
    sa.Column('order_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['route_id'], ['routes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item_context_modifiers',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('status', sa.String(length=32), nullable=False),
    sa.Column('item_id', sa.UUID(), nullable=True),
    sa.Column('price_id', sa.UUID(), nullable=True),
    sa.Column('catalog_context', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.ForeignKeyConstraint(['price_id'], ['prices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item_option_group',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('option_group_id', sa.UUID(), nullable=True),
    sa.Column('item_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.ForeignKeyConstraint(['option_group_id'], ['option_groups.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item_shifts',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.Column('monday', sa.Boolean(), nullable=False),
    sa.Column('tuesday', sa.Boolean(), nullable=False),
    sa.Column('wednesday', sa.Boolean(), nullable=False),
    sa.Column('thursday', sa.Boolean(), nullable=False),
    sa.Column('friday', sa.Boolean(), nullable=False),
    sa.Column('saturday', sa.Boolean(), nullable=False),
    sa.Column('sunday', sa.Boolean(), nullable=False),
    sa.Column('item_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('options',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('status', sa.String(length=16), nullable=True),
    sa.Column('index', sa.Integer(), nullable=True),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('external_code', sa.String(), nullable=True),
    sa.Column('option_group_id', sa.UUID(), nullable=True),
    sa.Column('product_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['option_group_id'], ['option_groups.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_items',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('item_id', sa.UUID(), nullable=True),
    sa.Column('order_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_item_options',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('order_item_id', sa.UUID(), nullable=True),
    sa.Column('product_option_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['order_item_id'], ['order_items.id'], ),
    sa.ForeignKeyConstraint(['product_option_id'], ['options.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_item_options')
    op.drop_table('order_items')
    op.drop_table('options')
    op.drop_table('item_shifts')
    op.drop_table('item_option_group')
    op.drop_table('item_context_modifiers')
    op.drop_table('route_orders')
    op.drop_table('order_totals')
    op.drop_table('order_schedules')
    op.drop_table('order_payments')
    op.drop_table('order_indoors')
    op.drop_table('order_deliveries')
    op.drop_table('order_customers')
    op.drop_table('order_benefits')
    op.drop_table('order_additional_fees')
    op.drop_table('option_groups')
    op.drop_table('items')
    op.drop_table('catalog_categories')
    op.drop_table('vehicles')
    op.drop_table('products')
    op.drop_table('orders')
    op.drop_table('merchant_users')
    op.drop_table('categories')
    op.drop_table('catalogs')
    op.drop_table('scale_prices')
    op.drop_table('routes')
    op.drop_table('merchants')
    op.drop_table('prices')
    op.drop_table('order_takeouts')
    op.drop_table('cvrps')
    op.drop_table('addresses')
    # ### end Alembic commands ###
