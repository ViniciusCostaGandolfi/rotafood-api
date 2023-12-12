from enum import Enum
from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship, Mapped
from config.database import Base
from restaurants.models.restaurant import Restaurant


class Role(Enum):
    OWNER = "OWNER"
    ADM = "ADM"
    GARSON = "GARSON"
    CHEF = "CHEF"
    DRIVER = "DRIVER"

 
class RestaurantUser(Base):
    __tablename__ = 'restaurant_user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    name = Column(String)
    phone = Column(String)
    permissions = Column(SQLEnum(Role))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant: Mapped[Restaurant] = relationship("Restaurant") 
