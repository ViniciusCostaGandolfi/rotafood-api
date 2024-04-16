from typing import List
from sqlalchemy import ARRAY, Column, String, ForeignKey, Integer, Float, Enum, Text
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID
import uuid

from api.core.database import Base
from api.domain.catalogs.models.product_dietary_restrictions import DietaryRestrictions
from api.domain.catalogs.models.option_group import OptionGroup
from api.domain.catalogs.models.selling_option import SellingOption
from api.domain.catalogs.models.serving_size import ServingSize
from api.domain.catalogs.models.weight_unit import WeightUnit


class Product(Base):
    __tablename__ = 'products'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)
    description = Column(String(1024))
    additional_information = Column(String(512))
    external_code = Column(String(255))
    image = Column(String(256))
    serving = Column(Enum(ServingSize))
    dietary_restrictions = Column(String(16))
    ean = Column(String(16))
    weight_quantity = Column(Float)
    weight_unit = Column(String(2), nullable=True)
    multiple_images = Column(ARRAY(String(256)))
    
    selling_option_id = Column(UUID(as_uuid=True), ForeignKey('selling_options.id'))
    selling_option: Mapped[SellingOption] = relationship("SellingOption", back_populates="product")
    
    option_groups: Mapped[List[OptionGroup]] = relationship("OptionGroup", back_populates="product", uselist=True)
