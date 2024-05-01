import uuid
from sqlalchemy import Column, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from api.config.database import Base
from sqlalchemy.dialects.postgresql import UUID


class OrderTotal(Base):
    __tablename__ = 'order_totals'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    benefits = Column(Numeric(10, 2))
    delivery_fee = Column(Numeric(10, 2))
    order_amount = Column(Numeric(10, 2))
    sub_total = Column(Numeric(10, 2))
    additional_fees = Column(Numeric(10, 2))
    order_id = Column(UUID(as_uuid=True), ForeignKey('order.id'))
    order = relationship("Order", back_populates="total")
