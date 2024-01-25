from pydantic import BaseModel, ConfigDict
from typing import List, Optional

from products.models.product import ProductType


class ProductOptionDto(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    external_code: str
    image_path: str
    price: float
    ean: str
    
    
    model_config = ConfigDict(from_attributes=True)
    


class ProductOptionGroupDto(BaseModel):
    id: Optional[int] = None
    name: str
    external_code: str
    status: str
    min_options: int
    max_options: int
    index: int
    product_opitions: List[ProductOptionDto]
    
    model_config = ConfigDict(from_attributes=True)


class CategoryDto(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    
    model_config = ConfigDict(from_attributes=True)

class ProductDto(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    additional_information: Optional[str] = None
    serving: Optional[str] = None
    dietary_restrictions: Optional[List[str]] = None
    weight_quantity: float
    weight_unit: str
    volume: float
    price: float
    product_type: ProductType
        
    
    image: Optional[str] = None
    multiple_images: Optional[List[str]] = None
    
    category: CategoryDto
    option_groups: Optional[List[ProductOptionGroupDto]] = None
    
    model_config = ConfigDict(from_attributes=True)

