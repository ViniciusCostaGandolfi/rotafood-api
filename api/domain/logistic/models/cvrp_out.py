from typing import List
from uuid import uuid4
from sqlalchemy import Column, ForeignKey, DECIMAL, Float
from sqlalchemy.dialects.postgresql import UUID
from api.config.database import Base
from sqlalchemy.orm import relationship, Mapped
from api.domain.logistic.models.cvrp_in import CvrpIn
from api.domain.logistic.models.route import Route


class CvrpOut(Base):
    __tablename__ = 'cvrp_outs'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    secconds_to_solve = Column(DECIMAL(precision=10, scale=3))
    total_discente_meters = Column(DECIMAL(precision=10, scale=3))

    cvrp_in_id = Column(ForeignKey('cvrp_ins.id'))
    cvrp_in = relationship('CvrpIn', uselist=False)
    
    routes = relationship('Route', uselist=True)
