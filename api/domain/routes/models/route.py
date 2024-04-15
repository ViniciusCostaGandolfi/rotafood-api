from enum import Enum
from sqlalchemy import ARRAY, VARCHAR, Column, Float, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship

from api.core.database import Base



class Route(Base):
    __tablename__ = 'routes'

    id = Column(Integer, autoincrement=True, primary_key=True)
    distance = Column(Float)
    volume = Column(Float)
    link_google_maps = Column(String)
    sequence = Column(ARRAY(Integer))
    merchant_id = Column(Integer, ForeignKey("merchants.id"))
    route_orders = relationship("RouteOrder", back_populates="route")

    
