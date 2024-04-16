from typing import Text
import uuid
from sqlalchemy import Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from api.core.database import Base
from sqlalchemy.dialects.postgresql import UUID


class OrderCommand(Base):
    __tablename__ = 'order_benefits'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(Text)
    target_id = Column(String)
    value = Column(Float)
    target = Column(String)
    order_id = Column(UUID(as_uuid=True), ForeignKey('order_details.id'))
    order = relationship("OrderDetails", back_populates="benefits")
    campaign_id = Column(UUID(as_uuid=True), ForeignKey('campaigns.id'))
    campaign = relationship("Campaign", back_populates="benefits")
