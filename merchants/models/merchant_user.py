from enum import Enum
from typing import Optional
from sqlalchemy import ARRAY, Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship, Mapped
from config.database import Base
from merchants.models.merchant import Merchant


class ModulePermissions(Enum):
    MERCHANT = 'MERCHANT'
    INTEGRATION = 'INTEGRATION'
    PRODUCTS = 'PRODUCTS'
    ORDERS = 'ORDERS'
    COMMANDS = 'COMMANDS'
    ROUTES = 'ROUTES'
    DRIVERS = 'DRIVERS'
    CATALOGS = 'CATALOGS'

    

 
class MerchantUser(Base):
    __tablename__ = 'merchant_users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    name = Column(String)
    phone = Column(String)
    permissions = Column(ARRAY(String), default=[e.value for e in ModulePermissions])
    merchant_id = Column(Integer, ForeignKey('merchants.id'))
    merchant: Mapped[Merchant] = relationship("Merchant") 
