from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from config.helpers import BaseModelCamel, to_camel

from products.models.product import ProductType


class ProductOptionDto(BaseModelCamel):
    id: Optional[int] = None
    name: str
    description: str
    external_code: str
    image_path: str
    price: float
    ean: str
    
    
    
    


class ProductOptionGroupDto(BaseModelCamel):
    id: Optional[int] = None
    name: str
    external_code: str
    status: str
    min_options: int
    max_options: int
    index: int
    product_opitions: List[ProductOptionDto]
    
    


class CategoryDto(BaseModelCamel):
    id: Optional[int] = None
    name: str
    description: str
    
    

class ProductDto(BaseModelCamel):
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
    
    

