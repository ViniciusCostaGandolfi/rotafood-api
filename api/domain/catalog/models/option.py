import uuid

from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from api.config.database import Base
from sqlalchemy.dialects.postgresql import UUID

class Option(Base):
    __tablename__ = 'options'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(String)
    index = Column(Integer)
    price = Column(Numeric(10, 2))
    external_code = Column(String)
    option_group_id = Column(UUID(as_uuid=True), ForeignKey('option_groups.id'))
    option_group = relationship("OptionGroup", back_populates="options")
    product_option = relationship("Product", uselist=False, back_populates="option")
