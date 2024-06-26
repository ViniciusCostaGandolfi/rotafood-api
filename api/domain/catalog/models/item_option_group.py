from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import relationship
from api.services.database_service import Base


class ItemOptionGroup(Base):
    __tablename__ = 'item_option_group'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    option_group_id = Column(UUID(as_uuid=True), ForeignKey('option_groups.id'))
    option_group = relationship('OptionGroup', back_populates='items')
    item_id = Column(UUID(as_uuid=True), ForeignKey('items.id'))
    item = relationship('Item', back_populates='option_groups')

   