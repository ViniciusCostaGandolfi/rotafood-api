
from sqlalchemy import ForeignKey, Column, Integer, String, Float, JSON
from sqlalchemy.orm import relationship

from database import Base



class ProductOptionAssotiation(Base):
    __tablename__ = 'product_option_associations'
    id = Column(Integer, autoincrement=True, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    productOption_group_id = Column(Integer, ForeignKey('product_option_groups.id'))
