from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship

from config.database import Base


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
    
    merchant_id = Column(Integer, ForeignKey('merchants.id'))
    merchant_user_id =  Column(Integer, ForeignKey('merchant_users.id'))
    customer_id = Column(Integer, ForeignKey('order_customers.id'))
    payment_id = Column(Integer, ForeignKey('order_payments.id'))
    delivery_id = Column(Integer, ForeignKey('order_deliveries.id'))

    customer = relationship("OrderCustomer", back_populates="orders")
    payment = relationship("OrderPayment", back_populates="order")
    delivery = relationship("OrderDelivery", back_populates="order")
    items = relationship("OrderItem", back_populates="order")
