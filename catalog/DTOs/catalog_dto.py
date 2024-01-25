from pydantic import BaseModel, ConfigDict, EmailStr
from config.to_camel import to_camel
from typing import List, Optional
from products.dtos.product_dto import ProductDTO


class CatalogItemDTO(BaseModel):
    id: Optional[int] = None
    merchant_id: int
    product_id: int
    product: ProductDTO
    
    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel)



class CatalogDTO(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    items: List[CatalogItemDTO]
    
    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel)

        