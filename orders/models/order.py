from enum import Enum
from sqlalchemy import Column, Float, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship, Mapped

from config.database import Base
from orders.models.order_delivery import OrderDelivery


class OrderType(Enum):
     DELIVERY = "DELIVERY"
     INDOOR = "INDOOR"
     TAKEOUT = "TAKEOUT"
     TABLE = "TABLE"

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, autoincrement=True, primary_key=True)
    order_type = Column(SQLEnum(OrderType))
    order_timing = Column(String)
    created_at = Column(DateTime)
    preparation_start_dateTime  = Column(DateTime)
    total_volume = Column(Float)
    total_price = Column(Float)
    
    merchant_id = Column(Integer, ForeignKey('merchants.id'))

    customer = relationship("OrderCustomer", back_populates="order")
    payment = relationship("OrderPayment", back_populates="order")
    delivery: Mapped[OrderDelivery] = relationship("OrderDelivery", back_populates="order")
    items = relationship("OrderItem", back_populates="order")
    route_order = relationship("ROuteOrder", back_populates="order")
