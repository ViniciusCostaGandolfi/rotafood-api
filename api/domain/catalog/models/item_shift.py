from datetime import datetime
from typing import TYPE_CHECKING, List
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship, Mapped
from api.config.database import Base

if TYPE_CHECKING:
    from api.domain.catalog.models.item import Item

class ItemShift(Base):
    __tablename__ = 'item_shifts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    start_time = Column(DateTime, nullable=False, default=datetime.now())
    end_time = Column(DateTime, nullable=False, default=datetime.now())
    monday = Column(Boolean(), nullable=False)
    tuesday = Column(Boolean(), nullable=False)
    wednesday = Column(Boolean(), nullable=False)
    thursday = Column(Boolean(), nullable=False)
    friday = Column(Boolean(), nullable=False)
    saturday = Column(Boolean(), nullable=False)
    sunday = Column(Boolean(), nullable=False)
    
    
    item_id = Column(UUID(as_uuid=True), ForeignKey('items.id'))
    
   