from uuid import UUID
import uuid

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from api.core.database import Base
from api.domain.catalog.models.status import Status # type: ignore

class Item(Base):
    __tablename__ = 'items'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String)
    status = Column(Enum(Status))
    external_code = Column(String)
    index = Column(Integer)
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'))
    category = relationship("Category", back_populates="items")
    option_groups = relationship("OptionGroup", back_populates="item")
    shifts = relationship("Shift", back_populates="item")
    context_modifiers = relationship("ItemContextModifier", back_populates="item")
    price = relationship("Price", back_populates="item", uselist=False)
