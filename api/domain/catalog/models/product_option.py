from uuid import UUID
import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from api.core.database import Base

class ProductOption(Base):
    __tablename__ = 'product_options'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False, length=2000)
    price_id = Column(UUID(as_uuid=True), ForeignKey('prices.id'))
    price = relationship("Price", back_populates="product_option", uselist=False)
    option_id = Column(UUID(as_uuid=True), ForeignKey('options.id'))
    option = relationship("Option", uselist=False, back_populates="product_option")