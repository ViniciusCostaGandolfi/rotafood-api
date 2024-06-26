from typing import Text
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from api.services.database_service import Base
from sqlalchemy.dialects.postgresql import UUID



class OrderItemOption(Base):
    __tablename__ = 'order_item_options'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_item_id = Column(UUID(as_uuid=True), ForeignKey('order_items.id'))
    order_item = relationship("OrderItem", back_populates="options")
    product_option_id = Column(UUID(as_uuid=True), ForeignKey('options.id'))
    product_option = relationship("ProductOption")