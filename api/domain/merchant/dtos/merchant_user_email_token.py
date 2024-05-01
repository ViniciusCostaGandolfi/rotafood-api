from typing import List
from pydantic import EmailStr
from api.config.pydantic import CustonModel
from api.domain.merchant.models.merchant_permission import MerchantPermission



class MerchantUserEmailToken(CustonModel):
    email: EmailStr
    permissions: List[MerchantPermission]
