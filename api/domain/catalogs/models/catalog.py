from enum import Enum
from sqlite3 import Date
from typing import List
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship, Mapped

from api.core.database import Base
from api.domain.catalogs.models.catalog_category import CatalogCategory


class Catalog(Base):
    __tablename__ = 'catalogs'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    modified_at = Column(DateTime, nullable=False)
    catalog_categories = relationship("CatalogCategory", back_populates="catalog", uselist=True)


