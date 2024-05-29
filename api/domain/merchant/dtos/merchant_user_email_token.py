from typing import List
from pydantic import EmailStr
from api.config.custom_model import CustomModel
from api.domain.merchant.models.merchant_permission import MerchantPermission



class MerchantUserEmailTokenDto(CustomModel):
    merchant_id: str
    email: EmailStr
    permissions: List[MerchantPermission]
