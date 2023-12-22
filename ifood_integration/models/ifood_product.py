from enum import Enum
from sqlalchemy import ARRAY, Column, ForeignKey, String, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship

from config.database import Base



class IFoodProduct(Base):
    __tablename__ = 'ifood_products'
    id = Column(Integer, autoincrement=True, primary_key=True)
    ifood_product_id = Column(String, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    
    product = relationship("Product", back_populates='ifood_product')