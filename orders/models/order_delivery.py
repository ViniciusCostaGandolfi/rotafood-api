from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from config.database import Base


class DeliveredBy(Enum):
    MERCHANT='MERCHANT'
    IFOOD='IFOOD'
    ROTAFOOD='ROTAFOOD'

class OrderDelivery(Base):
    __tablename__ = 'order_deliveries'

    id = Column(Integer, autoincrement=True, primary_key=True)
    pickup_code = Column(String)
    delivered_by = Column(String)
    delivery_dateTime = Column(DateTime)
    index = Column(Integer)

    address_id = Column(Integer, ForeignKey('addresses.id'))
    address = relationship("Address")