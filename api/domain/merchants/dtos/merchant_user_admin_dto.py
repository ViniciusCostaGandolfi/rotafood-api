from typing import List
from pydantic import EmailStr
from api.core.helpers import BaseModelCamel
from api.domain.merchants.models.merchant_user import ModulePermissions

class MerchantTokenCreationDto(BaseModelCamel):
    name: str
    phone: str
    password: str

class MerchantStaffRegistrationDto(BaseModelCamel):
    email: EmailStr
    permissions: List[ModulePermissions]
