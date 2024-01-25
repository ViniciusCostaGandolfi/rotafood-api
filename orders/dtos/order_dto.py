from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from addresses.dtos.address_dto import AddressDto
from ifood_integration.dtos.ifood_order_dto import IFoodOrderDto
from orders.models.order import OrderTimming, OrderType

from orders.models.order_delivery import OrderDeliveredBy
from products.dtos.product_dto import ProductDto, ProductOptionDto, ProductOptionGroupDto
import pytz



# class ProductDto(BaseModel):
#     id: Optional[int] = None
#     name: str
#     volume: float
#     price: float
#     description: Optional[str] = None
#     additional_information: Optional[str] = None
#     serving: Optional[str] = None
#     dietary_restrictions: Optional[List[str]] = None
#     image: Optional[str] = None
#     multiple_images: Optional[List[str]] = None
    
#     model_config = ConfigDict(from_attributes=True)
    
    

class OrderCustomerDto(BaseModel):

    id: Optional[int] = None
    name: str
    phone: str
    document_number: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
    
    

class OrderDeliveryDto(BaseModel):

    id: Optional[int] = None
    pickup_code: str
    delivered_by: OrderDeliveredBy
    delivery_datetime: Optional[datetime] = datetime.now(pytz.timezone('America/Sao_Paulo'))
    address: AddressDto
    
    model_config = ConfigDict(from_attributes=True)
    
    
    
# class ProductOptionDto(BaseModel):
#     id: Optional[int] = None
#     name: str
#     description: str
#     external_code: str
#     image_path: str
#     price: float
#     ean: str
    
#     model_config = ConfigDict(from_attributes=True)
    
    
# class ProductGroupOptionDto(BaseModel):
#     id: Optional[int] = None
#     name: str
#     external_code: str
#     status: str
#     min_options: int
#     max_options: int
    
    
class OrderItemOptionDto(BaseModel):
    id: Optional[int] = None
    product_option_group: Optional[ProductOptionGroupDto] = None
    product_option: Optional[ProductOptionDto] = None
    
    model_config = ConfigDict(from_attributes=True)
    

class OrderItemDto(BaseModel):

    id: Optional[int] = None
    quantity: int
    total_price: float
    total_volume: float
    product: ProductDto
    item_options: Optional[List[OrderItemOptionDto]] = None
    
    
    model_config = ConfigDict(from_attributes=True)
    
    
    
class OrderPaymentDto(BaseModel):
    id: Optional[int] = None
    method: str
    currency: str
    total_amount: float
    model_config = ConfigDict(from_attributes=True)
    
class OrderDto(BaseModel):

    id: Optional[int] = None
    
    order_type: OrderType
    order_timing: Optional[OrderTimming] = OrderTimming.IMMEDIATE.value
    created_at: Optional[datetime] = datetime.now(pytz.timezone('America/Sao_Paulo'))
    preparation_start_datetime : Optional[datetime] = datetime.now(pytz.timezone('America/Sao_Paulo'))
    total_volume: float
    total_price: float
    
    items: List[OrderItemDto]
    customer: Optional[OrderCustomerDto] = None
    payment: Optional[OrderPaymentDto] = None
    delivery: Optional[OrderDeliveryDto] = None
    ifood_order: Optional[IFoodOrderDto] = None
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)