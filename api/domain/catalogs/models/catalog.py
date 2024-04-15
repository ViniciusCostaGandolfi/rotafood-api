from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship

from api.core.database import Base


class Catalog(Base):
    __tablename__ = 'catalogs'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    description = Column(String)
    merchant_id = Column(Integer, ForeignKey('merchants.id'))

    merchant = relationship("Merchant")
    items = relationship("CatalogItem", back_populates="catalog")

