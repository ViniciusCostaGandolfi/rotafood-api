from sqlalchemy import ForeignKey, Column, Integer, String, Float, JSON
from sqlalchemy.orm import relationship

from config.database import Base


class ProductOption(Base):
    __tablename__ = 'product_options'
    id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)
    external_code = Column(String)
    image_path = Column(String)
    
    price_value = Column(Float)
    price_original_value = Column(Float)
    
    ean = Column(String)
    option_group_id = Column(String, ForeignKey('product_option_groups.id'))
