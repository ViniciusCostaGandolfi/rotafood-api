from typing import List
import uuid

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped
from api.core.database import Base
from api.domain.catalogs.models.item_context_modifier import ItemContextModifier
from api.domain.catalogs.models.price import Price
from api.domain.catalogs.models.item_shift import Shift
from api.domain.catalogs.models.status import Status
from sqlalchemy.dialects.postgresql import UUID

class Item(Base):
    __tablename__ = 'items'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String)
    status = Column(Enum(Status))
    external_code = Column(String)
    index = Column(Integer)
    
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'))
    category = relationship("Category", back_populates="items", uselist=True)
    
    product_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'))
    product = relationship("Product", back_populates="item", uselist=False)
    
    price_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'))
    price: Mapped[Price] = relationship("Price", back_populates="item", uselist=False)
        
    shifts: Mapped[List[Shift]] = relationship("Shift", back_populates="item")
    
    context_modifiers: Mapped[List[ItemContextModifier]] = relationship("ItemContextModifier", back_populates="item")
