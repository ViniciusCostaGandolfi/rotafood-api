from uuid import UUID
import uuid

from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from api.core.database import Base

class Option(Base):
    __tablename__ = 'options'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(String)
    index = Column(Integer)
    price = Column(Float)
    external_code = Column(String)
    option_group_id = Column(UUID(as_uuid=True), ForeignKey('option_groups.id'))
    option_group = relationship("OptionGroup", back_populates="options")
    product_option = relationship("ProductOption", uselist=False, back_populates="option")
