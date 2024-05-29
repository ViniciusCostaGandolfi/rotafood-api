from typing import List, Optional, Tuple
from uuid import uuid4
from api.config.custom_model import CustomModel
from pydantic import UUID4, Field
from api.domain.logistic.dtos.address_dto import AddressDto

class CoordinateDto(CustomModel):
    lat: float
    lon: float

class CvrpOrderDto(CustomModel):
    id: Optional[UUID4] = Field(default_factory=uuid4) 
    volume_liters: float
    created_at: int
    address: AddressDto
    
class CvrpBaseDto(CustomModel):
    id: Optional[UUID4] = Field(default_factory=uuid4) 
    address: AddressDto
    
class CvrpRouteDto(CustomModel):
    id: Optional[UUID4] = Field(default_factory=uuid4) 
    sequence: List[int]
    orders: List[CvrpOrderDto]
    route_line: List[CoordinateDto]
    distance_km: float
    volume_liters: float
    link_google_maps: str
 
class CvrpOutDto(CustomModel):
    id: Optional[UUID4] = Field(default_factory=uuid4) 
    base: CvrpBaseDto
    routes: List[CvrpRouteDto] 
    max_route_volume: float 
    max_route_orders: Optional[int] = None



class CvrpInDto(CustomModel):
    id: Optional[UUID4] = Field(default_factory=uuid4) 
    base: CvrpBaseDto
    orders: List[CvrpOrderDto]
    max_route_volume: float
    max_route_orders: Optional[int] = None  
 