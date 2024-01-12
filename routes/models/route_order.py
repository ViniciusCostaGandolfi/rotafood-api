from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship

from config.database import Base



class RouteOrder(Base):
    __tablename__ = 'route_orders'

    id = Column(Integer, autoincrement=True, primary_key=True)
    index = Column(Integer)
    route_id = Column(Integer, ForeignKey('routes.id'))
    order_id = Column(Integer, ForeignKey('orders.id'))
    route = relationship("Route", back_populates='route_orders')
    order = relationship("Order", back_populates="route_order")

