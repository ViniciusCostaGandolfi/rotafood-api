from sqlalchemy import ForeignKey, Column, Integer, String, Float
from sqlalchemy.orm import relationship

from config.database import Base


class Command(Base):
    __tablename__ = 'commands'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    table = Column(String)
    price = Column(Float)
    merchant_id = Column(Integer, ForeignKey('merchants.id'))
    orders = relationship('Order', back_populates='command', uselist=True)
