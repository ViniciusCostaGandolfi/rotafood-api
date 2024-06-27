from typing import TYPE_CHECKING, List
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from api.services.database_service import Base

if TYPE_CHECKING:
    from api.domain.catalog.models.product import Product
    from api.domain.merchant.models.merchant import Merchant

class ScalePrice(Base):
    __tablename__ = 'scale_prices'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    price = Column(Numeric(10, 2), nullable=False)
    min_quantity = Column(Integer(), nullable=False)
    
    price_id = Column(UUID(as_uuid=True), ForeignKey('prices.id'))