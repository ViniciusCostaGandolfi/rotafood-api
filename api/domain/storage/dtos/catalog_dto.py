from typing import List, Optional
from api.config.pydantic import BaseModelCamel
from api.domain.products.dtos.product_dto import ProductDto


class CatalogItemDTO(BaseModelCamel):
    id: Optional[int] = None
    merchant_id: int
    product_id: int
    product: ProductDto
    
   



class CatalogDTO(BaseModelCamel):
    id: Optional[int] = None
    name: str
    description: str
    items: List[CatalogItemDTO]
    
   

        