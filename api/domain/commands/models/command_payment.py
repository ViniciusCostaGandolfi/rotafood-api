import uuid
from xmlrpc.client import Boolean
from sqlalchemy import Column, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID

from api.core.database import Base
from api.domain.commands.models.command_payment_method import CommandPaymentMethod
from api.domain.merchants.models.merchant import Merchant


class CommandPayment(Base):
    __tablename__ = 'command_payments'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    method: CommandPaymentMethod = Column(String(16), nullable=False)
    paid = Column(Numeric(10, 2), nullable=False)
    pending = Column(Numeric(10, 2), nullable=False)