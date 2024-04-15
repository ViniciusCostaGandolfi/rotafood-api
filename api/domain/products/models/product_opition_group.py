from sqlalchemy import ForeignKey, Column, Integer, String, Float, JSON
from sqlalchemy.orm import relationship

from api.core.database import Base



class ProductOptionGroup(Base):
    __tablename__ = 'product_option_groups'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    external_code = Column(String)
    status = Column(String)
    index = Column(Integer)
    min_options = Column(Integer)
    max_options = Column(Integer)
    options = relationship('ProductOption', backref='option_group', cascade='all, delete-orphan')
    