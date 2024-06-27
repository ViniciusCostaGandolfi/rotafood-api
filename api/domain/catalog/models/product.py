from uuid import uuid4
from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from api.services.database_service import Base
from datetime import datetime

class Product(Base):
    __tablename__ = 'products'

    name = Column(String(30), nullable=False)


    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(64), nullable=False)
    description = Column(String(1024), nullable=False)
    ean = Column(String(256), nullable=False)
    additional_information = Column(String(1024), nullable=False)
    product_type = Column(String(32), nullable=False)
    dietary_restrictions = Column(ARRAY(String(32)))
    
    weight_unit = Column(String(8), nullable=False)
    weight = Column(Numeric(10, 2), nullable=False)
    
    volume_unit = Column(String(8), nullable=False)
    volume = Column(Numeric(10, 2), nullable=False)
    
    created_at = Column(DateTime, nullable=False, default=datetime.now())
        
    merchant_id = Column(UUID(as_uuid=True), ForeignKey('merchants.id'))
    merchant = relationship('Merchant', uselist=False)
    
