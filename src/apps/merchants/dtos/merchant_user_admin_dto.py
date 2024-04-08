from typing import List
from custom_model import EmailStr
from configs.helpers import BaseModelCamel
from merchants.models.merchant_user import ModulePermissions

class MerchantTokenCreationDto(BaseModelCamel):
    name: str
    phone: str
    password: str

class MerchantStaffRegistrationDto(BaseModelCamel):
    email: EmailStr
    permissions: List[ModulePermissions]
