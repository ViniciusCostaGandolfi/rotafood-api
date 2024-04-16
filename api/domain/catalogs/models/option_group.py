from sqlalchemy.dialects.postgresql import UUID
import uuid

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from api.core.database import Base

class OptionGroup(Base):
    __tablename__ = 'option_groups'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    status = Column(String)
    external_code = Column(String)
    index = Column(Integer)
    option_group_type = Column(String)
    item_id = Column(UUID(as_uuid=True), ForeignKey('items.id'))
    item = relationship("Item", back_populates="option_groups")
    options = relationship("Option", back_populates="option_group", cascade="all, delete-orphan")
