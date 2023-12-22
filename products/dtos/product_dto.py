from pydantic import BaseModel
from typing import List, Optional

from products.models.product import ProductType


class ProductOptionDTO(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    external_code: str
    image_path: str
    price: float
    ean: str


class ProductOptionGroupDTO(BaseModel):
    id: Optional[int] = None
    name: str
    external_code: str
    status: str
    min_options: int
    max_options: int
    index: int
    product_opitions: List[ProductOptionDTO]


class CategoryDTO(BaseModel):
    id: Optional[int] = None
    name: str
    description: str

class ProductDTO(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    additional_information: str
    serving: str
    dietary_restrictions: List[str]
    weight_quantity: float
    weight_unit: str
    volume: float
    price: float
    product_type: ProductType
    
    
    image: str
    multiple_images: List[str]
    
    category: CategoryDTO
    option_groups: List[ProductOptionGroupDTO]

