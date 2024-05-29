from datetime import datetime
from typing import TYPE_CHECKING, List
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship, Mapped
from api.services.database_service import Base

if TYPE_CHECKING:
    from api.domain.catalog.models.catalog_category import CatalogCategory
    from api.domain.merchant.models.merchant import Merchant

class Catalog(Base):
    __tablename__ = 'catalogs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    modified_at = Column(DateTime, nullable=False, default=datetime.now())
    catalog_context_modifier = Column(String(32), nullable=False)
    
    merchant_id = Column(UUID(as_uuid=True), ForeignKey('merchants.id'))
    merchant = relationship('Merchant', back_populates='catalogs')
    
    categories = relationship('CatalogCategory', back_populates='catalog')


    
