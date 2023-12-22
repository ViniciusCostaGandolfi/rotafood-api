from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base


class OrderCustomer(Base):
    __tablename__ = 'order_customers'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    phone = Column(String)
    document_number = Column(String)

    orders = relationship("Order", back_populates="customer")
