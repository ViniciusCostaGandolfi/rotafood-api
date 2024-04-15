from uuid import UUID
import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from api.core.database import Base



class Category(Base):
    __tablename__ = 'categories'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    catalog_categories = relationship("CatalogCategory", back_populates="category", cascade="all, delete-orphan")
    items = relationship("Item", back_populates="category")
