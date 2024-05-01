from typing import TYPE_CHECKING, List
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship, Mapped
from api.config.database import Base


class CatalogCategory(Base):
    __tablename__ = 'items'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    catalog_id = Column(UUID(as_uuid=True), ForeignKey('catalogs.id'))
    catalog = relationship('Catalog', back_populates='categories')
    
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'))
    category = relationship('category', back_populates='catalogs')
   