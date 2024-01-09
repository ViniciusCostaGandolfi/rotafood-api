from typing import List, Optional
from pydantic import BaseModel
from addresses.DTOs.address_dto import AddressDTO
from merchants.DTOs.merchant_dto import MerchantDTO

from orders.DTOs.order_dto import OrderDTO



class CVRPOrder(BaseModel):
    id: int
    total_volume: float
    address: AddressDTO
    
    class Config:
        from_attributes = True


class CVRPRoute(BaseModel):
    sequence: List[int]
    orders: List[CVRPOrder]
    distance: float
    volume: float
    link: str
    
    class Config:
        from_attributes = True
    
class CVRPIn(BaseModel):
    orders: List[CVRPOrder]
    origin: MerchantDTO
    drivers_volume: float
    
    class Config:
        from_attributes = True


class CVRPOut(BaseModel):
    routes: List[CVRPRoute]
    origin: MerchantDTO
    drivers_volume: float  
    
    class Config:
        from_attributes = True  
    

class RouteOrderDTO(BaseModel):
    id: Optional[int] = None
    index: int
    order: OrderDTO
    
    class Config:
        from_atributes = True

class RouteDTO(BaseModel):
    id: Optional[int] = None
    total_distance: float
    total_volume: float
    link_google_maps: str
    sequence: List[int]
    route_orders: List[RouteOrderDTO]
 
    class Config:
        from_atributes = True
    
