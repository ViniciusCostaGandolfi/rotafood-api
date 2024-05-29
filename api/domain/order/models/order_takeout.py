from sqlalchemy import Column, DateTime, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from api.services.database_service import Base


class OrderTakeout(Base):
    __tablename__ = 'order_takeouts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mode = Column(String(32))
    takeout_date_time = Column(DateTime)
    