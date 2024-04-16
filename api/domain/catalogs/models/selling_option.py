from sqlalchemy import ARRAY, Column, String, ForeignKey, Integer, Float, Enum, Text
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID
import uuid

from api.core.database import Base
from api.domain.catalogs.models.product_dietary_restrictions import DietaryRestrictions
from api.domain.catalogs.models.product import Product
from api.domain.catalogs.models.serving_size import ServingSize
from api.domain.catalogs.models.weight_unit import WeightUnit


class SellingOption(Base):
    __tablename__ = 'selling_options'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    minimum = Column(Float, nullable=False)
    incremental = Column(Float, nullable=False)
    available_units = Column(String(8), nullable=False)
    average_unit = Column(Float, nullable=False)
    product: Mapped[Product] = relationship("Product", back_populates="selling_option")
