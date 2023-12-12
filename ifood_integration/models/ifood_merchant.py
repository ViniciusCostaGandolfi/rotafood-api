from enum import Enum
from sqlalchemy import ARRAY, Column, ForeignKey, String, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship

from config.database import Base

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
    id = Column(Integer, autoincrement=True, primary_key=True)
    ifood_client_id = Column(String, primary_key=True)
    authorization_type = Column(SQLEnum(AuthorizationType))
    ifood_permissions = Column(ARRAY(SQLEnum(PermissionsType)))
    
    
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    
    restaurant = relationship("Restaurant", back_populates="ifood_merchant")