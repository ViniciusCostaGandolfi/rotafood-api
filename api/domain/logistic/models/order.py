from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, DateTime, ForeignKey, Integer, DECIMAL, Float, null
from sqlalchemy.dialects.postgresql import UUID
from api.services.database_service import Base
from sqlalchemy.orm import relationship, Mapped
from api.domain.logistic.models.address import Address


class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    total_volume_liters = Column(DECIMAL(precision=10, scale=3), nullable=True)
    total_weight_grams = Column(DECIMAL(precision=10, scale=3), nullable=True)
    toal_items_quantity = Column(Integer(), nullable=True)
    create_at = Column(DateTime(), default=datetime.now(), nullable=False)
    
    address_id = Column(ForeignKey('addresses.id'), nullable=False)
    address = relationship('Address', uselist=False)
    
    route_id = Column(ForeignKey('routes.id'), nullable=True)
    cvrp_in_id = Column(ForeignKey('cvrp_ins.id'), nullable=True)
    cvrptw_in_id = Column(ForeignKey('cvrptw_ins.id'), nullable=True)
    tsp_in_id = Column(ForeignKey('tsp_ins.id'), nullable=True)

