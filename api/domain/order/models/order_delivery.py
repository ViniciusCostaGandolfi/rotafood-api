from sqlalchemy import Column, DateTime, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from api.services.database_service import Base


class OrderDelivery(Base):
    __tablename__ = 'order_deliveries'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mode = Column(String)
    pickup_code = Column(String)
    delivered_by = Column(String)
    delivery_address_id = Column(UUID(as_uuid=True), ForeignKey('addresses.id'))
    delivery_address = relationship("Address")
    delivery_date_time = Column(DateTime)
    address_id = Column(UUID(as_uuid=True), ForeignKey('addresses.id'))
    address = relationship("Address")
    
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'))
    order = relationship("Order", back_populates="delivery")
