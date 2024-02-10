from pydantic import EmailStr
from config.helpers import BaseModelCamel
from merchants.models.merchant_user import MerchantUserRole

class MerchantTokenCreationDto(BaseModelCamel):
    name: str
    phone: str
    password: str

class MerchantStaffRegistrationDto(BaseModelCamel):
    email: EmailStr
    permissions: MerchantUserRole
