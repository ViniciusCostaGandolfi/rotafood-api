from enum import Enum
import uuid
from sqlalchemy import ARRAY, VARCHAR, Column, Float, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from api.core.database import Base



class Route(Base):
    __tablename__ = 'routes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    distance = Column(Float)
    volume = Column(Float)
    link_google_maps = Column(String)
    sequence = Column(ARRAY(Integer))
    merchant_id = Column(Integer, ForeignKey("merchants.id"))
    route_orders = relationship("RouteOrder", back_populates="route")

    
