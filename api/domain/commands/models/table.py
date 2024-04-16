from typing import List
import uuid
from sqlalchemy import ForeignKey, Column, Integer, Numeric, String
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID
from api.core.database import Base
from api.domain.commands.models.command import Command
from api.domain.merchants.models.merchant import Merchant

class Table(Base):
    __tablename__ = 'table'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)    
    name = Column(String(64), nullable=False)
    
    paid = Column(Numeric(10, 2), nullable=False)
    pending = Column(Numeric(10, 2), nullable=False)
    
    merchant_id = Column(Integer, ForeignKey('merchants.id'))
    merchant: Mapped[Merchant] = relationship('Merchant', uselist=False)
    commands: Mapped[List[Command]] = relationship('Command', back_populates='table', uselist=True)
