from datetime import datetime
from typing import List, Optional

from pydantic import UUID4
from api.config.custom_model import CustomModel
from api.domain.storage.dtos.image_dto import ImageDto
    
    

class ProductDto(CustomModel):
    id: Optional[UUID4] = None
    name: str
    description: str
    ean: str
    additional_information: str
    product_type: str
    dietary_restrictions: List[str]
    weight_unit: str
    weight: float
    volume_unit: str
    volume: float
    created_at: datetime
    image: ImageDto

class ProductCreateDto(CustomModel):
    name: str
    description: str
    ean: str
    additional_information: str
    product_type: str
    dietary_restrictions: List[str]
    weight_unit: str
    weight: float
    volume_unit: str
    volume: float

class ProductUpdateDto(CustomModel):
    name: Optional[str] = None
    description: Optional[str] = None
    ean: Optional[str] = None
    additional_information: Optional[str] = None
    product_type: Optional[str] = None
    dietary_restrictions: Optional[List[str]] = None
    weight_unit: Optional[str] = None
    weight: Optional[float] = None
    volume_unit: Optional[str] = None
    volume: Optional[float] = None
