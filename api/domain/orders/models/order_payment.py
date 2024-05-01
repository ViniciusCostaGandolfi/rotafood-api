import uuid
from sqlalchemy import Boolean, Column, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from api.config.database import Base
from api.domain.orders.models.order_payment_type import OrderPaymentType


class OrderPayment(Base):
    __tablename__ = 'order_payments'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    method = Column(String)
    prepaid = Column(Boolean)
    currency = Column(String)
    type = Column(String)
    value = Column(Numeric(10, 2))
    order_id = Column(UUID(as_uuid=True), ForeignKey('order_details.id'))
    order = relationship("OrderDetails", back_populates="payments")