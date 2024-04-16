from sqlalchemy import ARRAY, Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship, Mapped
from api.core.database import Base
from api.domain.merchants.models.merchant import Merchant
from api.domain.merchants.models.module_permissions import ModulePermissions

 
class MerchantUser(Base):
    __tablename__ = 'merchant_users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    email = Column(String(128), unique=True, nullable=True)
    password = Column(String(128), nullable=False)
    name = Column(String(64), nullable=False)
    phone = Column(String(16), nullable=False)
    permissions = Column(ARRAY(String(16)), default=[e.value for e in ModulePermissions])
    
    merchant_id = Column(Integer, ForeignKey('merchants.id'))
    merchant: Mapped[Merchant] = relationship("Merchant") 
