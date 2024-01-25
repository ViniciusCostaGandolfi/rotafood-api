from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from addresses.dtos.address_dto import AddressDto
from merchants.dtos.merchant_dto import MerchantDto

from orders.dtos.order_dto import OrderDto



class CVRPOrder(BaseModel):
    id: Optional[int] = None
    total_volume: float
    address: AddressDto
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class CVRPRoute(BaseModel):
    id: Optional[int] = None
    sequence: List[int]
    orders: List[CVRPOrder]
    distance: float
    volume: float
    link_google_maps: str
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    
class CVRPIn(BaseModel):
    orders: List[CVRPOrder]
    merchant: MerchantDto
    drivers_volume: float
     
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class CVRPOut(BaseModel):
    merchant: MerchantDto
    routes: List[CVRPRoute]
    drivers_volume: float  
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    

class RouteOrderDto(BaseModel):
    id: Optional[int] = None
    index: int
    order: OrderDto
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class RouteDto(BaseModel):
    id: Optional[int] = None
    distance: float
    volume: float
    link_google_maps: str
    sequence: List[int]
    route_orders: List[RouteOrderDto]
 
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
