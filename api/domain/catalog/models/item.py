from datetime import datetime
from uuid import uuid4
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import relationship
from api.services.database_service import Base


class Item(Base):
    __tablename__ = 'items'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    type = Column(String(64), nullable=False)
    status = Column(String(16), nullable=False)
    index = Column(Integer, nullable=False)
    dietary_restrictions = Column(ARRAY(String(32)))
    
    created_at = Column(DateTime, nullable=False, default=datetime.now())

    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'))
    product = relationship('Product', uselist=False)
    
    price_id = Column(UUID(as_uuid=True), ForeignKey('prices.id'))
    price = relationship('Price', uselist=False)

    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'))
    category = relationship('Category', uselist=False)

    merchant_id = Column(UUID(as_uuid=True), ForeignKey('merchants.id'))
    merchant = relationship('Merchant', uselist=False)

    shifts = relationship('ItemShift', uselist=True)
    option_groups = relationship('ItemOptionGroup', uselist=True)
    context_modifiers = relationship('ItemContextModifier', uselist=True)
