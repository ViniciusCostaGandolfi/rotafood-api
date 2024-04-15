from uuid import UUID
import uuid

from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from api.core.database import Base

class Price(Base):
    __tablename__ = 'prices'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    value = Column(Float)
    original_value = Column(Float)
    item = relationship("Item", back_populates="price", uselist=False)
    scale_prices = relationship("ScalePrice", back_populates="price")
