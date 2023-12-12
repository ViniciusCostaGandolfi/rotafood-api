from enum import Enum
from sqlalchemy import ARRAY, Column, ForeignKey, String, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship

from config.database import Base



class IFoodOrder(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    ifood_order_id = Column(String, primary_key=True)
    
    order_id = Column(Integer, ForeignKey('orders.id'))
    
    order = relationship("Order", back_populates="ifood_order")