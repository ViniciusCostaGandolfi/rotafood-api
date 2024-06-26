from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Integer, String
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import relationship
from api.services.database_service import Base




class Category(Base):
    __tablename__ = 'categories'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(64), nullable=False)
    status = Column(String(16), nullable=False)
    index = Column(Integer, nullable=False)
    template = Column(String(16), nullable=False)
    merchant_id = Column(UUID(as_uuid=True), ForeignKey('merchants.id'))
    merchant = relationship('Merchant', back_populates='items', uselist=False)
    
    catalogs = relationship('CatalogCategory', back_populates='categories', uselist=True)
    items = relationship('Item', back_populates='category', uselist=True)
    
