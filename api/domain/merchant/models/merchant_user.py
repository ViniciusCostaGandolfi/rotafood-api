from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from api.services.database_service import Base



class MerchantUser(Base):
    __tablename__ = 'merchant_users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255))
    email = Column(String(255), unique=True)
    password = Column(String(255))
    phone = Column(String(255))
    permissions = Column(ARRAY(String(64)))

    merchant_id = Column(UUID(as_uuid=True), ForeignKey('merchants.id'))
    merchant = relationship('Merchant', back_populates='merchant_users')
