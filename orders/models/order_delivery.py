from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from config.database import Base


class Delivery(Base):
    __tablename__ = 'order_deliveries'

    id = Column(Integer, primary_key=True)
    mode = Column(String)
    pickupCode = Column(String)
    deliveredBy = Column(String)
    deliveryDateTime = Column(DateTime)

    address_id = Column(Integer, ForeignKey('address.id'))
    address = relationship("Address")