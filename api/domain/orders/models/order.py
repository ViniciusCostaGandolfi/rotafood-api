from typing import List, Text
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from api.core.database import Base
from sqlalchemy.dialects.postgresql import UUID

from api.domain.ifood_integration.dtos.ifood_order_detail import AdditionalFee, Merchant
from api.domain.orders.models.order_benefict import OrderBenefit
from api.domain.orders.models.order_customer import OrderCustomer
from api.domain.orders.models.order_delivery import OrderDelivery
from api.domain.orders.models.order_indoor import OrderIndoor
from api.domain.orders.models.order_item import OrderItem
from api.domain.orders.models.order_payment import OrderPayment
from api.domain.orders.models.order_sales_chanel import OrderSalesChannel
from api.domain.orders.models.order_schedule import OrderSchedule
from api.domain.orders.models.order_takeout import OrderTakeout
from api.domain.orders.models.order_timing import OrderTiming
from api.domain.orders.models.order_total import OrderTotal
from api.domain.orders.models.order_type import OrderType



class Order(Base):
    __tablename__ = 'orders'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_type: OrderType = Column(String)
    created_at = Column(DateTime)
    preparation_start_date_time = Column(DateTime)
    sales_channel: OrderSalesChannel = Column(String)
    order_timing: OrderTiming = Column(String)
    extra_info = Column(Text)
    
    merchant_id = Column(UUID(as_uuid=True), ForeignKey('merchants.id'))
    merchant: Merchant = relationship("Merchant", uselist=False, back_populates="order")
    
    total_id = Column(UUID(as_uuid=True), ForeignKey('order_totals.id'))
    total: OrderTotal = relationship("Total", uselist=False, back_populates="order")
    
    customer_id = Column(UUID(as_uuid=True), ForeignKey('order_customers.id'))
    customer: OrderCustomer = relationship("OrderCustomer", uselist=False, back_populates="order")
    
    delivery_id = Column(UUID(as_uuid=True), ForeignKey('order_deliveries.id'))
    delivery: OrderDelivery = relationship("OrderDelivery", uselist=False, back_populates="order")
    
    schedule_id = Column(UUID(as_uuid=True), ForeignKey('order_totals.id'))
    schedule: OrderSchedule = relationship("OrderSchedule", uselist=False, back_populates="order")
    
    indoor_id = Column(UUID(as_uuid=True), ForeignKey('order_indoors.id'))
    indoor: OrderIndoor = relationship("OrderIndoor", uselist=False, back_populates="order")
    
    takeout_id = Column(UUID(as_uuid=True), ForeignKey('order_takeouts.id'))
    takeout: OrderTakeout = relationship("OrderTakeout", uselist=False, back_populates="order")
    
    benefits: List[OrderBenefit] = relationship("OrderBenefit", back_populates="order")
    
    payments: List[OrderPayment] = relationship("OrderPayment", back_populates="order")
    
    items: List[OrderItem] = relationship("OrderItem", back_populates="order")
    
    additional_fees: List[AdditionalFee] = relationship("OrderAdditionalFee", back_populates="order")

