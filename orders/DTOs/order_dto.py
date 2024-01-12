from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from addresses.DTOs.address_dto import AddressDTO
from orders.models.order import OrderTimming, OrderType

from orders.models.order_delivery import OrderDeliveredBy
from products.dtos.product_dto import ProductDTO, ProductOptionDTO, ProductOptionGroupDTO
import pytz



# class ProductDTO(BaseModel):
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
    
    

class OrderCustomerDTO(BaseModel):

    id: Optional[int] = None
    name: str
    phone: str
    document_number: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
    
    

class OrderDeliveryDTO(BaseModel):

    id: Optional[int] = None
    pickup_code: str
    delivered_by: OrderDeliveredBy
    delivery_datetime: Optional[datetime] = datetime.now(pytz.timezone('America/Sao_Paulo'))
    address: AddressDTO
    
    model_config = ConfigDict(from_attributes=True)
    
    
    
# class ProductOptionDTO(BaseModel):
#     id: Optional[int] = None
#     name: str
#     description: str
#     external_code: str
#     image_path: str
#     price: float
#     ean: str
    
#     model_config = ConfigDict(from_attributes=True)
    
    
# class ProductGroupOptionDTO(BaseModel):
#     id: Optional[int] = None
#     name: str
#     external_code: str
#     status: str
#     min_options: int
#     max_options: int
    
    
class OrderItemOptionDTO(BaseModel):
    id: Optional[int] = None
    product_option_group: Optional[ProductOptionGroupDTO] = None
    product_option: Optional[ProductOptionDTO] = None
    
    model_config = ConfigDict(from_attributes=True)
    

class OrderItemDTO(BaseModel):

    id: Optional[int] = None
    quantity: int
    total_price: float
    total_volume: float
    product: ProductDTO
    item_options: Optional[List[OrderItemOptionDTO]] = None
    
    
    model_config = ConfigDict(from_attributes=True)
    
    
    
class OrderPaymentDTO(BaseModel):
    id: Optional[int] = None
    method: str
    currency: str
    total_amount: float
    model_config = ConfigDict(from_attributes=True)
    
class OrderDTO(BaseModel):

    id: Optional[int] = None
    
    order_type: OrderType
    order_timing: Optional[OrderTimming] = OrderTimming.IMMEDIATE.value
    created_at: Optional[datetime] = datetime.now(pytz.timezone('America/Sao_Paulo'))
    preparation_start_datetime : Optional[datetime] = datetime.now(pytz.timezone('America/Sao_Paulo'))
    total_volume: float
    total_price: float
    
    items: List[OrderItemDTO]
    customer: Optional[OrderCustomerDTO] = None
    payment: Optional[OrderPaymentDTO] = None
    delivery: Optional[OrderDeliveryDTO] = None
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)