from typing import TYPE_CHECKING
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from api.config.database import Base

class Image(Base):
    __tablename__ = 'images'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    url = Column(String(1024), nullable=False)
    origin = Column(String(32), nullable=False)
     
    merchant_id = Column(UUID(as_uuid=True), ForeignKey('merchants.id'))
    merchant = relationship('Merchant', back_populates='images')
