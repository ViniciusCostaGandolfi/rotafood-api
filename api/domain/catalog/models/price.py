from typing import TYPE_CHECKING, List
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship, Mapped
from api.config.database import Base

if TYPE_CHECKING:
    from api.domain.catalog.models.scale_price import ScalePrice

class Price(Base):
    __tablename__ = 'prices'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    value = Column(Numeric(10, 2), nullable=False)
    original_value = Column(Numeric(10, 2), nullable=False)
    
    scale_prices = relationship("ScalePrice", back_populates="price", uselist=True)
