from datetime import datetime
from uuid import uuid4
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from api.services.database_service import Base


class Catalog(Base):
    __tablename__ = 'catalogs'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    modified_at = Column(DateTime, nullable=False, default=datetime.now())
    catalog_context_modifier = Column(String(32), nullable=False)
    merchant_id = Column(UUID(as_uuid=True), ForeignKey('merchants.id'))
    merchant = relationship('Merchant')
    categories = relationship('CatalogCategory', back_populates='catalog') 