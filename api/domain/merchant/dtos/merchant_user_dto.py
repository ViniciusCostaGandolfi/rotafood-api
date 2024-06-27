from typing import List, Optional
from pydantic import UUID4, EmailStr
from api.config.custom_model import CustomModel
from api.domain.merchant.dtos.merchant_dto import MerchantDto
from api.domain.merchant.models.merchant_permission import MerchantPermission




class MerchantUserDto(CustomModel):
    id: Optional[UUID4] = None
    name: str
    email: EmailStr
    password: str
    phone: str
    permissions: List[MerchantPermission]
    merchant: MerchantDto