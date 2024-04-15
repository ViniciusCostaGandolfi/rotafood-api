from uuid import UUID
import uuid
from sqlalchemy import Column, ForeignKey
from api.core.database import Base
from sqlalchemy.orm import relationship


class CatalogCategory(Base):
    __tablename__ = 'catalog_category'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    catalog_id = Column(UUID(as_uuid=True), ForeignKey('catalogs.id'))
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'))
    catalog = relationship("Catalog", back_populates="catalog_categories")
    category = relationship("Category", back_populates="catalog_categories")
