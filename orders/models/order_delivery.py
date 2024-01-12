from email.policy import default
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz

from config.database import Base

class OrderDeliveredBy(Enum):
    IFOOD = 'IFOOD'
    MERCHANT = 'MERCHANT'
    ROTAFOOD = 'ROTAFOOD'

class OrderDelivery(Base):
    __tablename__ = 'order_deliveries'

    id = Column(Integer, autoincrement=True, primary_key=True)
    pickup_code = Column(String)
    delivered_by = Column(SQLEnum(OrderDeliveredBy))
    delivery_datetime = Column(DateTime(timezone=True))    
    address_id = Column(Integer, ForeignKey('addresses.id'))
    order_id = Column(Integer, ForeignKey('orders.id'))
    address = relationship("Address")
    order = relationship("Order", back_populates="delivery", single_parent=True)
    
    # Correção aqui
