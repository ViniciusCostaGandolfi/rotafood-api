import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from api.services.database_service import Base
from sqlalchemy.dialects.postgresql import UUID



class Order(Base):
    __tablename__ = 'orders'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_type = Column(String)
    created_at = Column(DateTime)
    preparation_start_date_time = Column(DateTime)
    sales_channel = Column(String)
    order_timing = Column(String)
    extra_info = Column(String)
    
    merchant_id = Column(UUID(as_uuid=True), ForeignKey('merchants.id'))
    merchant = relationship("Merchant", back_populates="order", uselist=False)
    
    total = relationship("OrderTotal", back_populates="order", uselist=False)
    
    customer = relationship("OrderCustomer", back_populates="order", uselist=False)
    
    delivery = relationship("OrderDelivery", back_populates="order", uselist=False)
    
    schedule = relationship("OrderSchedule", back_populates="order", uselist=False)
    
    indoor = relationship("OrderIndoor", back_populates="order", uselist=False)
    
    takeout = relationship("OrderTakeout", back_populates="order", uselist=False)
    
    payment = relationship("OrderPayment", back_populates="order", uselist=False)
    
    benefits = relationship("OrderBenefit", back_populates="order", uselist=False)
    
    
    items = relationship("OrderItem", back_populates="order", uselist=True)
    
    additional_fees = relationship("OrderAdditionalFee", back_populates="order", uselist=True)

