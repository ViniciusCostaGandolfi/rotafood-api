from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship

from database import Base


class CatalogItem(Base):
    __tablename__ = 'catalog_items'

    id = Column(Integer, autoincrement=True, primary_key=True)
    catalog_id = Column(Integer, ForeignKey('catalogs.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product")
    catalog = relationship('Catalog', back_populates='items')

