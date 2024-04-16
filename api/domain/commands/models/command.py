from datetime import datetime
from decimal import Decimal
import uuid
from sqlalchemy import DateTime, ForeignKey, Column, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from api.core.database import Base


class Command(Base):
    __tablename__ = 'commands'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(64), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now())
    
    payment_id = Column(UUID, ForeignKey('command_payments.id'))
    payment = relationship('CommandPayment', uselist=True)
    
    table_id = Column(UUID, ForeignKey('command_tables.id'))
    table = relationship('CommandTable', uselist=False)
    
    merchant_id = Column(UUID, ForeignKey('merchants.id'))
    merchant = relationship('Merchant', uselist=False)
    
    orders = relationship('Order', back_populates='command', uselist=True)
