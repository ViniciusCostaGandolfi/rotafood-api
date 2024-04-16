from sqlalchemy import Column, DateTime, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from api.core.database import Base
from api.domain.orders.models.order_indoor_mode import OrderIndoorMode


class OrderIndoor(Base):
    __tablename__ = 'order_indoors'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mode: OrderIndoorMode = Column(String)
    delivery_date_time = Column(DateTime)
    table = Column(String)
