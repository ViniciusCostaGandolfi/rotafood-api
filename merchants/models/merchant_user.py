from enum import Enum
from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship, Mapped
from config.database import Base
from merchants.models.merchant import Merchant


class MerchantUserRole(Enum):
    OWNER = "OWNER"
    ADM = "ADM"
    GARSON = "GARSON"
    CHEF = "CHEF"
    DRIVER = "DRIVER"

 
class MerchantUser(Base):
    __tablename__ = 'merchant_users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    name = Column(String)
    phone = Column(String)
    permissions = Column(SQLEnum(MerchantUserRole))
    merchant_id = Column(Integer, ForeignKey('merchants.id'))
    merchant: Mapped[Merchant] = relationship("Merchant") 
