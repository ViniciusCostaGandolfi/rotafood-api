from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship

from config.database import Base


class OrderDeliveredBy(Enum):
    MERCHANT='MERCHANT'
    IFOOD='IFOOD'
    ROTAFOOD='ROTAFOOD'

class OrderDelivery(Base):
    __tablename__ = 'order_deliveries'

    id = Column(Integer, autoincrement=True, primary_key=True)
    pickup_code = Column(String)
    delivered_by = Column(SQLEnum(OrderDeliveredBy))
    delivery_dateTime = Column(DateTime)    
    address_id = Column(Integer, ForeignKey('addresses.id'))
    order_id = Column(Integer, ForeignKey('orders.id'))
    
    address = relationship("Address")
    order = relationship("Order")
    route_order = relationship("RouteOrder", back_populates="order_delivery")

