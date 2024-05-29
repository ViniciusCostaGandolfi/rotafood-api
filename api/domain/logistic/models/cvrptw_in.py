from datetime import datetime
from typing import List
from uuid import uuid4
from sqlalchemy import Column, DateTime, ForeignKey, Integer, DECIMAL, Float
from sqlalchemy.dialects.postgresql import UUID
from api.services.database_service import Base
from sqlalchemy.orm import relationship, Mapped
from api.domain.logistic.models.route_order import RouteOrder


class CvrpIn(Base):
    __tablename__ = 'cvrp_ins'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    create_at = Column(DateTime(), default=datetime.now(), nullable=False)
    
