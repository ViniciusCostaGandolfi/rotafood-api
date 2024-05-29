from uuid import uuid4
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.dialects.postgresql import UUID
from api.services.database_service import Base


class Address(Base):
    __tablename__ = 'addresses'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    street_name = Column(String(length=64))
    formatted_address = Column(String(length=64), nullable=False)
    street_number = Column(String(length=64), nullable=False)
    city = Column(String(length=64), nullable=False)
    postal_code = Column(String(length=64), nullable=False)
    neighborhood = Column(String(length=64), nullable=False)
    state = Column(String(length=64), nullable=False)
    complement = Column(String(length=64), nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
