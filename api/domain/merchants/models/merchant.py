from typing import List
from uuid import uuid4
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID
from api.core.database import Base
from api.domain.addresses.models.address import Address
from api.domain.catalogs.models.catalog import Catalog


class Merchant(Base):
    __tablename__ = 'merchants'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(128), nullable=False)
    description = Column(String(length=1024), nullable=False)
    document_type = Column(String(4), nullable=False)
    document = Column(String(16), nullable=False)
    
    address_id = Column(Integer, ForeignKey('addresses.id'))
    address: Mapped[Address] = relationship('Address')