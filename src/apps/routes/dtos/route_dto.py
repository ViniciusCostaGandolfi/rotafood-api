from typing import List, Optional, Tuple
from custom_model import BaseModel, ConfigDict
from addresses.dtos.address_dto import AddressDto
from configs.helpers import BaseModelCamel, to_camel
from merchants.dtos.merchant_dto import MerchantDto

from orders.dtos.order_dto import OrderDto



class CVRPOrder(BaseModelCamel):
    id: Optional[int] = None
    total_volume: float
    address: AddressDto
    

class CVRPRoute(BaseModelCamel):
    id: Optional[int] = None
    sequence: List[int]
    orders: List[CVRPOrder]
    distance: float
    points: List[Tuple[float, float]]
    volume: float
    link_google_maps: str
        
class CVRPIn(BaseModelCamel):
    orders: List[CVRPOrder]
    merchant: MerchantDto 
    drivers_volume: float
     

class CVRPOut(BaseModelCamel):
    merchant: MerchantDto
    routes: List[CVRPRoute]
    drivers_volume: float  
        

class RouteOrderDto(BaseModelCamel):
    id: Optional[int] = None
    index: int
    order: OrderDto
    

class RouteDto(BaseModelCamel):
    id: Optional[int] = None
    distance: float
    volume: float
    link_google_maps: str
    sequence: List[int]
    route_orders: List[RouteOrderDto]
 