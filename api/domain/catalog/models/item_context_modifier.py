from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from api.services.database_service import Base


class ItemContextModifier(Base):
    __tablename__ = 'item_context_modifiers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    status = Column(String(32), nullable=False)
    
    item_id = Column(UUID(as_uuid=True), ForeignKey('items.id'))
    
    price_id = Column(UUID(as_uuid=True), ForeignKey('prices.id'))
    price = relationship('Price', back_populates='items', uselist=False)
    
    catalog_context = Column(String(64), nullable=False)
    
