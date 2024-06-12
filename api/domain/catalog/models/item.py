from typing import TYPE_CHECKING, List
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from api.services.database_service import Base


class Item(Base):
    __tablename__ = 'items'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    type = Column(String(64), nullable=False)
    status = Column(String(1024), nullable=False)
    index = Column(Integer, nullable=False)
    dietary_restrictions = Column(ARRAY(String(32)))
    
    
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'))
    product = relationship('Product', back_populates='items', uselist=False)
    
    price_id = Column(UUID(as_uuid=True), ForeignKey('prices.id'))
    price = relationship('Price', back_populates='items', uselist=False)
    
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'))
    category = relationship('Category', back_populates='items', uselist=False)
    
    merchant_id = Column(UUID(as_uuid=True), ForeignKey('merchants.id'))
    merchant = relationship('Merchant', back_populates='items', uselist=False)
    
    shifits = relationship('ItemShift', back_populates='items', uselist=True)
    option_groups = relationship('OptionGroups', back_populates='items', uselist=True)
    context_modifiers = relationship('ItemContextModifier', back_populates='items', uselist=True)
    merchant = relationship('Merchant', back_populates='items', uselist=True)

    
