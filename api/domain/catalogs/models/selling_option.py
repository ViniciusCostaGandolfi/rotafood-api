from sqlalchemy import ARRAY, Column, String, ForeignKey, Integer, Float, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from api.core.database import Base


class SellingOption(Base):
    __tablename__ = 'selling_options'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    minimum = Column(Float, nullable=False)
    incremental = Column(Float, nullable=False)
    available_units = Column(String(8), nullable=False)
    average_unit = Column(Float, nullable=False)
    product = relationship("Product", back_populates="selling_option")
