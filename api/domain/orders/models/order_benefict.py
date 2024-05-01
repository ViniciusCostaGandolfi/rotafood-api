from typing import Text
import uuid
from sqlalchemy import Column, DateTime, Float, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship
from api.config.database import Base
from sqlalchemy.dialects.postgresql import UUID


class OrderBenefit(Base):
    __tablename__ = 'order_benefits'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(String(32))
    value = Column(Numeric(10, 2))
    target = Column(String(32))
    order_id = Column(UUID(as_uuid=True), ForeignKey('order_details.id'))
    order = relationship("OrderDetails", back_populates="benefits")
