from datetime import datetime
from typing import List
from uuid import uuid4
from sqlalchemy import Column, DateTime, ForeignKey, Integer, DECIMAL, Float
from sqlalchemy.dialects.postgresql import UUID
from api.services.database_service import Base
from sqlalchemy.orm import relationship
from api.domain.logistic.models.route_order import RouteOrder


class Cvrp(Base):
    __tablename__ = 'cvrps'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    secconds_to_solve = Column(DECIMAL(precision=10, scale=3))
    total_discente_meters = Column(DECIMAL(precision=10, scale=3))
    routes = relationship('Route', uselist=True)