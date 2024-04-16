from typing import List
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID
from api.core.database import Base
from api.domain.catalogs.models.status import Status
import uuid

class Item(Base):
    __tablename__ = 'items'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String)
    status = Column(Enum(Status))
    external_code = Column(String)
    index = Column(Integer)
    
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'))
    category = relationship("Category", back_populates="items", uselist=False)
    
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'))  # Assuming there's a 'products' table
    product = relationship("Product", back_populates="items", uselist=False)
    
    price_id = Column(UUID(as_uuid=True), ForeignKey('prices.id'))  # Assuming there's a 'prices' table
    price = relationship("Price", back_populates="items", uselist=False)
    
    shifts = relationship("Shift", back_populates="item")
    context_modifiers = relationship("ItemContextModifier", back_populates="item")
