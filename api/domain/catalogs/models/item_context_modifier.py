from typing import List
import uuid

from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped
from api.core.database import Base
from api.domain.catalogs.models.price import Price
from api.domain.catalogs.models.status import Status
from sqlalchemy.dialects.postgresql import UUID

class ItemContextModifier(Base):
    __tablename__ = 'item_context_modifiers'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(String(16), nullable=False)
    price_id = Column(UUID(as_uuid=True), ForeignKey('prices.id'))
    price: Mapped[Price] = relationship("Price")
    external_code = Column(String(255), nullable=True)
    catalog_context = Column(String(255), nullable=False)