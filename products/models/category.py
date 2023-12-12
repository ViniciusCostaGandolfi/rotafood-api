from sqlalchemy import ForeignKey, create_engine, Column, Integer, String, Float, JSON
from sqlalchemy.orm import relationship

from config.database import Base

class Category(Base):
    __tablename__ = 'categories'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)