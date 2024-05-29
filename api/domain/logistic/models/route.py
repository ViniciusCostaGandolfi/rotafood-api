from datetime import datetime
from typing import List
from uuid import uuid4
from sqlalchemy import Column, DateTime, ForeignKey, Integer, DECIMAL, Float, String
from sqlalchemy.dialects.postgresql import UUID
from api.services.database_service import Base
from sqlalchemy.orm import relationship, Mapped
from api.domain.logistic.models.route_order import RouteOrder


class Route(Base):
    __tablename__ = 'routes'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    type = Column(String(length=16))
    total_volume_liters = Column(DECIMAL(precision=10, scale=3), nullable=False)
    total_weight_grams = Column(DECIMAL(precision=10, scale=3), nullable=False)
    toal_items_quantity = Column(Integer(), nullable=False)
    total_distance_meters = Column(DECIMAL(precision=10, scale=3), nullable=False)
    create_at = Column(DateTime(), default=datetime.now(), nullable=False)
    orders: Mapped[List['RouteOrder']] = relationship('RouteOrder', uselist=True, back_populates='route')

    cvrp_out_id = Column(ForeignKey('cvrp_outs.id'), nullable=True)
    cvrptw_out_id = Column(ForeignKey('cvrptw_outs.id'), nullable=True)
    tsp_out_id = Column(ForeignKey('tsp_outs.id'), nullable=True)