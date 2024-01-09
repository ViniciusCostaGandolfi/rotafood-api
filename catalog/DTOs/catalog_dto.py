from pydantic import BaseModel, EmailStr
from merchants.DTOs.merchant_dto import MerchantDTO
from typing import List, Optional
from merchants.models.merchant_user import MerchantUserRole
from products.dtos.product_dto import ProductDTO


class CatalogItemDTO(BaseModel):
    id: Optional[int] = None
    merchant_id: int
    product_id: int
    product: ProductDTO
    
    class Config:
        from_attributes = True


class CatalogDTO(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    items: List[CatalogItemDTO]
    
    class Config:
        from_attributes = True
        