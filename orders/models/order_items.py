from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from config.database import Base

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer)
    total_price = Column(Float)
    total_volume = Column(Float)
    
    order_id = Column(Integer, ForeignKey('orders.id'))
    order = relationship("Order")
    
    order_item_opition = relationship('OrderItemOption')



