from typing import TYPE_CHECKING, List
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship, Mapped
from api.config.database import Base

if TYPE_CHECKING:
    from api.domain.catalog.models.item_context_modifier import ItemContextModifier
    from api.domain.catalog.models.category import Category
    from api.domain.catalog.models.item_shift import ItemShift
    from api.domain.catalog.models.price import Price
    from api.domain.catalog.models.product import Product
    from api.domain.merchant.models.merchant import Merchant

class Item(Base):
    __tablename__ = 'items'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    type = Column(String(64), nullable=False)
    status = Column(String(1024), nullable=False)
    index = Column(Integer(), nullable=False)
    product_type = Column(String(32), nullable=False)
    dietary_restrictions = Column(ARRAY(String(32)))
    
    
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'))
    product = relationship('product', back_populates='items', uselist=False)
    
    price_id = Column(UUID(as_uuid=True), ForeignKey('prices.id'))
    price = relationship('price', back_populates='items', uselist=False)
    
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'))
    category = relationship('category', back_populates='items', uselist=False)
    
    merchant_id = Column(UUID(as_uuid=True), ForeignKey('merchants.id'))
    merchant = relationship('Merchant', back_populates='items', uselist=False)
    
    shifits = relationship('ItemShift', back_populates='items', uselist=True)
    context_modifiers = relationship('ItemContextModifier', back_populates='items', uselist=True)
    merchant = relationship('Merchant', back_populates='items', uselist=True)

    