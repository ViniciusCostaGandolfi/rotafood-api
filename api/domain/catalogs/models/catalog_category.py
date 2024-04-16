from uuid import UUID
import uuid
from sqlalchemy import Column, ForeignKey
from api.core.database import Base
from sqlalchemy.orm import relationship

from api.domain.catalogs.models.category import Category


class CatalogCategory(Base):
    __tablename__ = 'catalog_category'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    catalog_id = Column(UUID(as_uuid=True), ForeignKey('catalogs.id'))
    catalog = relationship("Catalog", back_populates="catalog_categories")
    
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'))
    category: Category = relationship("Category", back_populates="catalog_categories")
