from sqlalchemy import Column, DateTime, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from api.core.database import Base
from api.domain.orders.models.order_indoor_mode import OrderIndoorMode
from api.domain.orders.models.order_takeout_mode import OrderTakeoutMode


class OrderTakeout(Base):
    __tablename__ = 'order_takeouts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mode: OrderTakeoutMode = Column(String)
    takeout_date_time = Column(DateTime)