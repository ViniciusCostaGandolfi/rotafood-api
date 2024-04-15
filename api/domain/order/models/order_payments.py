from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from api.core.database import Base


class OrderPayment(Base):
    __tablename__ = 'order_payments'

    id = Column(Integer, autoincrement=True, primary_key=True)
    method = Column(String)
    currency = Column(String)
    total_amount = Column(Float)
    order_id = Column(Integer, ForeignKey('orders.id'))
    order = relationship("Order", back_populates="payment", single_parent=True)
