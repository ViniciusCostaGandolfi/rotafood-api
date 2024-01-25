from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from addresses.models.address import Address
from catalog.models.catalog import Catalog
from config.database import Base
from ifood_integration.models.ifood_merchant import IFoodMerchant 

class Merchant(Base):
    __tablename__ = 'merchants'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    document_type = Column(String)
    document = Column(String)
    address_id = Column(Integer, ForeignKey('addresses.id'))
 
    address: Mapped[Address] = relationship("Address")
    catalogs: Mapped[Catalog] = relationship('Catalog', back_populates='merchant')
    ifood_merchant: Mapped[IFoodMerchant] = relationship('IFoodMerchant', back_populates='merchant')
