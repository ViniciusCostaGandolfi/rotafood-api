import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID
from api.core.database import Base
from api.domain.catalogs.models.catalog import Catalog
from api.domain.catalogs.models.product import Product


class CatalogItem(Base):
    __tablename__ = 'catalog_items'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    product_id = Column(UUID, ForeignKey('products.id'))
    product: Mapped[Product] = relationship("Product")
    
    catalog_id = Column(UUID, ForeignKey('catalogs.id'))
    catalog: Mapped[Catalog] = relationship('Catalog', back_populates='items')

