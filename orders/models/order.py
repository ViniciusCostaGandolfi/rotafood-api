from enum import Enum
from sqlalchemy import Column, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import ENUM
from commands.models.command import Command
from config.database import Base


class OrderType(Enum):
     DELIVERY = "DELIVERY"
     INDOOR = "INDOOR"
     TAKEOUT = "TAKEOUT"
     TABLE = "TABLE"
     
class OrderTimming(Enum):
     IMMEDIATE = "IMMEDIATE"
     SCHEDULED = "SCHEDULED" 

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, autoincrement=True, primary_key=True)
    order_type = Column(ENUM(OrderType))
    order_timing = Column(ENUM(OrderTimming))
    created_at = Column(DateTime(timezone=True))
    preparation_start_datetime  = Column(DateTime(timezone=True))
    total_volume = Column(Float)
    total_price = Column(Float)
    
    merchant_id = Column(Integer, ForeignKey('merchants.id'))
     
    command_id = Column(Integer, ForeignKey('commands.id'))
    command: Mapped[Command] = relationship("Command") 

    customer = relationship("OrderCustomer", back_populates="order", uselist=False)
    payment = relationship("OrderPayment", back_populates="order", uselist=False)
    delivery = relationship("OrderDelivery", back_populates="order", uselist=False)
    route_order = relationship("RouteOrder", back_populates="order", uselist=False)
    ifood_order = relationship("IFoodOrder", uselist=False)
    items = relationship("OrderItem", back_populates="order", uselist=True)
    
    
