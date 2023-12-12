from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base 

class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    document_type = Column(String)
    document = Column(String)
    address_id = Column(Integer, ForeignKey('address.id'))
 
    address = relationship("Address") #type:ignore
