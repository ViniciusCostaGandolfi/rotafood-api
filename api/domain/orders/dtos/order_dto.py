from typing import List, Optional
from datetime import datetime
from api.config.pydantic import BaseModelCamel
from api.domain.addresses.dtos.address_dto import AddressDto
from api.domain.ifood_integration.dtos.ifood_order_dto import IFoodOrderDto
from api.domain.orders.models.order import OrderTimming, OrderType
from api.domain.orders.models.order_delivery import OrderDeliveredBy
from api.domain.products.dtos.product_dto import ProductDto, ProductOptionDto, ProductOptionGroupDto
import pytz

    
    

class OrderCustomerDto(BaseModelCamel):

    id: Optional[int] = None
    name: str
    phone: str
    document_number: Optional[str] = None
    
    
    
    

class OrderDeliveryDto(BaseModelCamel):

    id: Optional[int] = None
    pickup_code: str
    delivered_by: OrderDeliveredBy
    delivery_datetime: Optional[datetime] = datetime.now(pytz.timezone('America/Sao_Paulo'))
    address: AddressDto
    
    
    
    
    
# class ProductOptionDto(BaseModelCamel):
#     id: Optional[int] = None
#     name: str
#     description: str
#     external_code: str
#     image_path: str
#     price: float
#     ean: str
    
#     
    
    
# class ProductGroupOptionDto(BaseModelCamel):
#     id: Optional[int] = None
#     name: str
#     external_code: str
#     status: str
#     min_options: int
#     max_options: int
    
    
class OrderItemOptionDto(BaseModelCamel):
    id: Optional[int] = None
    product_option_group: Optional[ProductOptionGroupDto] = None
    product_option: Optional[ProductOptionDto] = None
    
    
    

class OrderItemDto(BaseModelCamel):

    id: Optional[int] = None
    quantity: int
    total_price: float
    total_volume: float
    product: ProductDto
    item_options: Optional[List[OrderItemOptionDto]] = None
    
    
    
    
    
    
class OrderPaymentDto(BaseModelCamel):
    id: Optional[int] = None
    method: str
    currency: str
    total_amount: float
    
    
class OrderDto(BaseModelCamel):

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
    
    