from sqlalchemy import Column, Integer, String, Float
from config.database import Base


class Address(Base):
    __tablename__ = 'address'
 
    id = Column(Integer, primary_key=True)
    number = Column(String(16), nullable=True)
    street = Column(String(255))
    neighborhood = Column(String(255), nullable=True)
    city = Column(String(100))
    state = Column(String(100))
    postal_code = Column(String(20))
    lat = Column(Float)
    lon = Column(Float)
