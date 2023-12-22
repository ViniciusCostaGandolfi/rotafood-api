from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base


class OrderPayment(Base):
    __tablename__ = 'order_payments'

    id = Column(Integer, autoincrement=True, primary_key=True)
    method = Column(String)
    currency = Column(String)
    total_amount = Column(Float)

    order = relationship("Order", back_populates="payment")
