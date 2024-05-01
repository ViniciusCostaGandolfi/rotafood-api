from typing import TYPE_CHECKING, List
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship, Mapped
from api.config.database import Base
from api.domain.catalog.models.item import Item

if TYPE_CHECKING:
    from api.domain.catalog.models.category import Category
    from api.domain.catalog.models.item_shift import ItemShift
    from api.domain.catalog.models.price import Price
    from api.domain.catalog.models.product import Product
    from api.domain.merchant.models.merchant import Merchant

class ItemContextModifier(Base):
    __tablename__ = 'items'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    status = Column(String(32), nullable=False)
    
    item_id = Column(UUID(as_uuid=True), ForeignKey('items.id'))
    
    price_id = Column(UUID(as_uuid=True), ForeignKey('prices.id'))
    price = relationship('price', back_populates='items', uselist=False)
    
    catalog_context = Column(String(64), nullable=False)
    
