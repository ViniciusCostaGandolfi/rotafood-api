from typing import List
import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID
from api.core.database import Base
from api.domain.catalogs.models.item import Item



class Category(Base):
    __tablename__ = 'categories'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    catalog_categories = relationship("CatalogCategory", back_populates="category", cascade="all, delete-orphan")
    items: Mapped[List[Item]] = relationship("Item", back_populates="category")
