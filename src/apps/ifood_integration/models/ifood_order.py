from enum import Enum
from sqlalchemy import ARRAY, Column, ForeignKey, String, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship

from database import Base



class IFoodOrder(Base):
    __tablename__ = 'ifood_orders'
    id = Column(Integer, autoincrement=True, primary_key=True)
    
    order_from_ifood_id = Column(String, primary_key=True)
    
    order_id = Column(Integer, ForeignKey('orders.id'))
    
    # order = relationship("Order", back_populates="ifood_order")