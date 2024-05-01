

from typing import List

from pydantic import EmailStr
from api.config.pydantic import CustonModel
from api.domain.merchant.dtos.merchant_dto import MerchantDto
from api.domain.merchant.dtos.merchant_user_dto import MerchantUserDto
from api.domain.merchant.models.merchant_permission import MerchantPermission




class EmailTokenPayloadDto(CustonModel):
    merchant_id: str
    permissions: List[MerchantPermission]
    email: EmailStr
    exp: float