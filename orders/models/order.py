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

    id = Column(String, primary_key=True)
    order_type = Column(SQLEnum(OrderType))
    order_timing = Column(String)
    created_at = Column(DateTime)
    preparation_start_dateTime  = Column(DateTime)
    
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    restaurant_user_id =  Column(Integer, ForeignKey('restaurant_users.id'))
    address_id = Column(Integer, ForeignKey('address.id'))
    customer_id = Column(Integer, ForeignKey('order_customers.id'))
    payment_id = Column(Integer, ForeignKey('order_payments.id'))
    delivery_id = Column(Integer, ForeignKey('deliveries.id'))

    customer = relationship("OrderCustomer", back_populates="orders")
    address = relationship("Address", back_populates="order")
    payment = relationship("OrderPayment", back_populates="order")
    delivery = relationship("OrderDelivery", back_populates="order")
    items = relationship("OrderItem", back_populates="order")
