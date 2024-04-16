from enum import Enum
from sqlalchemy import ARRAY, Column, ForeignKey, String, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship

from api.core.database import Base

class AuthorizationType(Enum):
    NOT_SENDED="NOT_SENDED"
    WAITING="WAITING"
    AUTHORIZED="AUTHORIZED"
    
class PermissionsType(Enum):
    MERCHANT="MERCHANT"
    CATALOG="CATALOG"
    FINANCIAL="FINANCIAL"
    ORDERS="ORDERS"

class IFoodMerchant(Base):
    __tablename__ = 'ifood_merchants'

    id = Column(Integer, autoincrement=True, primary_key=True)
    ifood_client_id = Column(String, primary_key=True)
    authorization_type = Column(SQLEnum(AuthorizationType))
    ifood_permissions = Column(ARRAY(SQLEnum(PermissionsType)))
    
    
    merchant_id = Column(Integer, ForeignKey('merchants.id'))
    
    merchant = relationship("Merchant", back_populates="ifood_merchant")