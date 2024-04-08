from enum import Enum
from sqlalchemy import ForeignKey, Column, Integer, String, Float, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from database import Base


class ProductType(Enum):
    REGULAR = "REGULAR"
    IFOOD = "IFOOD"
    # AIQFOME = "AIQFOME"


# Defina a tabela de produtos
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    additional_information = Column(String)
    serving = Column(String)
    dietary_restrictions = Column(ARRAY(String)) 
    weight_quantity = Column(Float)
    weight_unit = Column(String)
    product_type = Column(SQLEnum(ProductType))
    price = Column(Float)
    
    volume = Column(Float)
    
    image = Column(String)
    multiple_images = Column(ARRAY(String))
    

    category_id = Column(Integer, ForeignKey('product_categories.id'))
    merchant_id = Column(Integer, ForeignKey('merchants.id'))
    
    category = relationship('ProductCategory', backref='products')
    option_groups = relationship('ProductOptionGroup', secondary='product_option_associations', backref='product')
    ifood_product = relationship('IFoodProduct', back_populates="product", uselist=False)

