from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from api.core.database import Base

class OrderItemOption(Base):
    __tablename__ = 'order_item_options'

    id = Column(Integer, primary_key=True, autoincrement=True)  
    order_item_id = Column(Integer, ForeignKey('order_items.id'))
    
    product_option_id = Column(Integer, ForeignKey('product_options.id'))
    product_option = relationship('ProductOption')
    
    product_option_group_id = Column(Integer, ForeignKey('product_option_groups.id'))
    product_option_group = relationship('ProductOptionGroup')


