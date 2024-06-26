from typing import Text
import uuid
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from api.services.database_service import Base
from sqlalchemy.dialects.postgresql import UUID

class OrderCustomer(Base):
    __tablename__ = 'order_customers'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    document_number = Column(String)
    phone_number = Column(String)
    segmentation = Column(String)
    orders_count_on_merchant = Column(Integer)
    
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'))
    order = relationship("Order", back_populates="customer")