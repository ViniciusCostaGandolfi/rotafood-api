from typing import List
from pydantic import EmailStr
from api.config.custom_model import CustomModel
from api.domain.merchant.dtos.merchant_dto import MerchantDto
from api.domain.merchant.models.merchant_permission import MerchantPermission




class MerchantUserDto(CustomModel):
    name: str
    email: EmailStr
    password: str
    phone: str
    document: str
    permissions: List[MerchantPermission]
    merchant: MerchantDto