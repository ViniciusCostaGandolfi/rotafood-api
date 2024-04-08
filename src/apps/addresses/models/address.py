from sqlalchemy import Column, Integer, String, Float
from database import Base





class Address(Base):
    __tablename__ = 'addresses'
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    street_name = Column(String)
    formatted_address = Column(String)
    street_number = Column(String)
    city = Column(String)
    postal_code = Column(String)
    neighborhood = Column(String)
    state = Column(String)
    complement = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
