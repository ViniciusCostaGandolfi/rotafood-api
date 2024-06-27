from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Numeric
from sqlalchemy.orm import relationship
from api.services.database_service import Base


class Price(Base):
    __tablename__ = 'prices'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    value = Column(Numeric(10, 2), nullable=False)
    original_value = Column(Numeric(10, 2), nullable=False)
    
    scale_prices = relationship("ScalePrice", uselist=True)
