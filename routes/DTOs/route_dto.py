from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from addresses.DTOs.address_dto import AddressDTO
from merchants.DTOs.merchant_dto import MerchantDTO

from orders.DTOs.order_dto import OrderDTO



class CVRPOrder(BaseModel):
    id: int
    total_volume: float
    address: AddressDTO
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class CVRPRoute(BaseModel):
    sequence: List[int]
    orders: List[CVRPOrder]
    distance: float
    volume: float
    link_google_maps: str
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    
class CVRPIn(BaseModel):
    orders: List[CVRPOrder]
    origin: MerchantDTO
    drivers_volume: float
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class CVRPOut(BaseModel):
    routes: List[CVRPRoute]
    origin: MerchantDTO
    drivers_volume: float  
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    

class RouteOrderDTO(BaseModel):
    id: Optional[int] = None
    index: int
    order: OrderDTO
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class RouteDTO(BaseModel):
    id: Optional[int] = None
    distance: float
    volume: float
    link_google_maps: str
    sequence: List[int]
    route_orders: List[RouteOrderDTO]
 
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
