from sqlalchemy import ForeignKey, create_engine, Column, Integer, String, Float, JSON
from sqlalchemy.orm import relationship

from config.database import Base

class ProductCategory(Base):
    __tablename__ = 'product_categories'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    merchant_id = Column(Integer, ForeignKey("merchants.id"))