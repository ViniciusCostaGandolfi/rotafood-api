from enum import Enum
from sqlalchemy import ForeignKey, Column, String, Float, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from config.database import Base


class ProductType(Enum):
    REGULAR = "REGULAR"
    IFOOD = "IFOOD"


# Defina a tabela de produtos
class Product(Base):
    __tablename__ = 'products'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    additional_information = Column(String)
    serving = Column(String)
    dietary_restrictions = Column(ARRAY(String))
    weight_quantity = Column(Float)
    weight_unit = Column(String)
    product_type = Column(SQLEnum(ProductType))
    
    volume = Column(Float)
    
    image = Column(String)
    multiple_images = Column(ARRAY(String))
    

    category_id = Column(String, ForeignKey('product_categories.id'))
    restaurant_id = Column(String, ForeignKey('restaurants.id'))
    
    category = relationship('ProductCategory', backref='products')
    option_groups = relationship('ProductOptionGroup', backref='product', cascade='all, delete-orphan')

