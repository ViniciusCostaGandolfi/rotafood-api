from sqlalchemy import Column, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from api.core.database import Base


class OrderAdditionalFee(Base):
    __tablename__ = 'order_additional_fees'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String(255), nullable=False)
    value = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    full_description = Column(Text, nullable=True)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'), nullable=False)
    order = relationship("Order", back_populates="additional_fees")