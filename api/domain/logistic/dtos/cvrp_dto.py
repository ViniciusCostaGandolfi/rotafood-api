from typing import List, Optional, Tuple
import uuid
from api.config.pydantic import CustonModel
from api.domain.logistic.dtos.address_dto import AddressDto


class CvrpOrderDto(CustonModel):
    id: Optional[str] = str(uuid.uuid4()) 
    total_volume: float
    create_at: int
    address: AddressDto
    
class CvrpBaseDto(CustonModel):
    id: Optional[str] = str(uuid.uuid4()) 
    address: AddressDto
    
class CvrpRouteDto(CustonModel):
    id: Optional[str] = str(uuid.uuid4()) 
    sequence: List[int]
    orders: List[CvrpOrderDto]
    route_line: List[Tuple[float, float]]
    distance_in_km: float
    total_volume: float
    max_route_orders: Optional[int] = None
    link_google_maps: str

class CvrpOutDto(CustonModel):
    id: Optional[str] = str(uuid.uuid4()) 
    base: CvrpBaseDto
    routes: List[CvrpRouteDto]
    max_route_volume: float
    max_route_orders: Optional[int] = None


class CvrpInDto(CustonModel):
    id: Optional[str] = str(uuid.uuid4()) 
    base: CvrpBaseDto
    orders: List[CvrpOrderDto]
    max_route_volume: float
    max_route_orders: Optional[int] = None
