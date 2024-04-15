from sqlite3 import Time
from uuid import UUID
import uuid
from xmlrpc.client import Boolean

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from api.core.database import Base

class Shift(Base):
    __tablename__ = 'shifts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    start_time = Column(Time)
    end_time = Column(Time)
    monday = Column(Boolean, default=False)
    tuesday = Column(Boolean, default=False)
    wednesday = Column(Boolean, default=False)
    thursday = Column(Boolean, default=False)
    friday = Column(Boolean, default=False)
    saturday = Column(Boolean, default=False)
    sunday = Column(Boolean, default=False)
    item_id = Column(UUID(as_uuid=True), ForeignKey('items.id'))
    item = relationship("Item", back_populates="shifts")