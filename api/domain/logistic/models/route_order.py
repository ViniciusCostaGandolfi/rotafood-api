from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, DateTime, ForeignKey, Integer, DECIMAL, Float
from sqlalchemy.dialects.postgresql import UUID
from api.services.database_service import Base
from sqlalchemy.orm import relationship, Mapped
from api.domain.logistic.models.address import Address
from api.domain.logistic.models.order import Order


class RouteOrder(Base):
    __tablename__ = 'route_orders'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    
    route_id = Column(ForeignKey('routes.id'))
    route = relationship('Route', uselist=False)
    
    order_id = Column(ForeignKey('orders.id'))
    order: Mapped['Order'] = relationship('Order', uselist=False)
