from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from addresses.DTOs.address_dto import AddressDTO
from orders.models.order import OrderType

from orders.models.order_delivery import DeliveredBy
from products.dtos.product_dto import ProductOptionDTO


class OrderCustomerDTO(BaseModel):

    id: Optional[int] = None
    name: str
    phone: str
    document_number: Optional[str] = None
    

class OrderDeliveryDTO(BaseModel):

    id: Optional[int] = None
    pickup_code: str
    delivered_by: DeliveredBy
    delivery_dateTime: datetime
    index: int
    address: AddressDTO
    
    
class ProductOptionGroupDTO(BaseModel):
    id: Optional[int] = None
    name: str
    external_code: str
    status: str
    min_options: int
    max_options: int
    index: int
    

class OrderItemDTO(BaseModel):

    id: Optional[int] = None
    product_group_option: ProductOptionGroupDTO
    product_option: ProductOptionDTO
    
    
class OrderPaymentDTO(BaseModel):
    id: Optional[int] = None
    method: str
    currency: str
    total_amount: float
    
    
class OrderDTO(BaseModel):

    id: Optional[int] = None
    
    order_type: OrderType
    order_timing: str
    created_at: datetime
    preparation_start_dateTime : datetime
    total_volume: float
    total_price: float
    
    items: List[OrderItemDTO]
    customer: Optional[OrderCustomerDTO] = None
    payment: Optional[OrderPaymentDTO] = None
    delivery: Optional[OrderDeliveryDTO] = None