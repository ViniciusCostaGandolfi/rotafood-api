from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import relationship
from api.services.database_service import Base




class CatalogCategory(Base):
    __tablename__ = 'catalog_categories'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    catalog_id = Column(UUID(as_uuid=True), ForeignKey('catalogs.id'))
    catalog = relationship('Catalog', back_populates='categories')
    
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'))
    category = relationship('Category', back_populates='catalogs')
   