from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from api.services.database_service import Base
from datetime import datetime


class Merchant(Base):
    __tablename__ = 'merchants'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(64), nullable=False)
    corporate_name = Column(String(64), nullable=False)
    description = Column(String(256), nullable=False)
    document_type = Column(String(4), nullable=False)
    document = Column(String(16), nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.now())
    
    address_id = Column(UUID(as_uuid=True), ForeignKey('addresses.id'))
    address = relationship('Address', uselist=False)
    
    merchant_users = relationship('MerchantUser', back_populates='merchant', uselist=True)
