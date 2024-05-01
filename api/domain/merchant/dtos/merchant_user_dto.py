from typing import List
from pydantic import EmailStr
from api.config.pydantic import CustonModel
from api.domain.merchant.dtos.merchant_dto import MerchantDto
from api.domain.merchant.models.merchant_permission import MerchantPermission




class MerchantUserDto(CustonModel):
    name: str
    email: EmailStr
    password: str
    phone: str
    document: str
    permissions: List[MerchantPermission]
    merchant: MerchantDto