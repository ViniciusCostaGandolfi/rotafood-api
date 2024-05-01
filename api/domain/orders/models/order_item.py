from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from api.config.database import Base
import uuid

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quantity = Column(Integer)
    item_id = Column(UUID(as_uuid=True), ForeignKey('items.id'))
    item = relationship("Item") 
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'))
    order = relationship("Order", back_populates="items")
    options = relationship("OrderItemOption", back_populates="order_item")

