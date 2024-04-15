import logging

# Configurar logger para este módulo
logger = logging.getLogger(__name__)

# Informação sobre importação do módulo
logger.info(f"Importando Merchant de {__file__}")


from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from api.domain.addresses.models.address import Address
from api.core.database import Base
from api.domain.catalogs.models.catalog import Catalog
from api.domain.ifood_integration.models.ifood_merchant import IFoodMerchant 


class Merchant(Base):
    __tablename__ = 'merchants'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    document_type = Column(String)
    document = Column(String)
    address_id = Column(Integer, ForeignKey('addresses.id'))
 
    address: Mapped[Address] = relationship("Address")
    catalogs: Mapped[Catalog] = relationship('Catalog', back_populates='merchant')
    ifood_merchant: Mapped[IFoodMerchant] = relationship('IFoodMerchant', back_populates='merchant')
