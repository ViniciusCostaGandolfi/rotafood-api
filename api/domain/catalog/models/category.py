from typing import TYPE_CHECKING, List
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship, Mapped
from api.config.database import Base


if TYPE_CHECKING:
    from api.domain.catalog.models.item import Item
    from api.domain.merchant.models.merchant import Merchant
    from api.domain.catalog.models.catalog_category import CatalogCategory


class Category(Base):
    __tablename__ = 'categories'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(64), nullable=False)
    
    merchant_id = Column(UUID(as_uuid=True), ForeignKey('merchants.id'))
    merchant = relationship('Merchant', back_populates='items', uselist=False)
    
    catalogs = relationship('CatalogCategory', back_populates='categories', uselist=True)
    items = relationship('Item', back_populates='category', uselist=True)
    
