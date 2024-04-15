from enum import Enum
from sqlite3 import Date
from uuid import UUID
import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship

from api.core.database import Base


class Catalog(Base):
    __tablename__ = 'catalogs'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    modified_at = Column(Date)
    catalog_categories = relationship("CatalogCategory", 
                                      back_populates="catalog", 
                                      cascade="all, delete-orphan", 
                                      uselist=True)


