from sqlalchemy import ForeignKey, Column, Integer, String, Float, JSON
from sqlalchemy.orm import relationship

from api.core.database import Base


class ProductOption(Base):
    __tablename__ = 'product_options'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    description = Column(String)
    external_code = Column(String)
    image_path = Column(String)
    
    price = Column(Float)
    ean = Column(String)
    product_option_group_id = Column(Integer, ForeignKey('product_option_groups.id'))
    
