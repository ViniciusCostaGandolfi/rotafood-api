from uuid import uuid4
from sqlalchemy import DECIMAL, Column, ForeignKey, Integer, String, Float
from sqlalchemy.dialects.postgresql import UUID
from api.services.database_service import Base


class Vehicle(Base):
    __tablename__ = 'vehicles'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name =  Column(String(length=128), nullable=True)
    km_per_liter = Column(DECIMAL(precision=10, scale=3), nullable=True)
    max_volume_liters = Column(DECIMAL(precision=10, scale=3), nullable=True)
    max_weight_grams = Column(DECIMAL(precision=10, scale=3), nullable=True)
    max_items_quantity = Column(Integer(), nullable=True)
    max_distance_meters = Column(DECIMAL(precision=10, scale=3), nullable=True)
    
    cvrp_in_id = Column(ForeignKey('cvrp_ins.id'))
    route_id = Column(ForeignKey('routes.id'))

