from sqlalchemy import Column, DateTime, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from api.core.database import Base


class OrderSchedule(Base):
    __tablename__ = 'order_schedules'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    delivery_date_time_start = Column(DateTime)
    delivery_date_time_end = Column(DateTime)