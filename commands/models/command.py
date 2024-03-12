from sqlalchemy import ForeignKey, Column, Integer, String, Float
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, Mapped

from config.database import Base
from orders.models.order import Order
from products.models.product import Product


class Command(Base):
    __tablename__ = 'commands'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    table = Column(String)
    price = Column(Float)
    merchant_id = Column(Integer, ForeignKey('merchants.id'))