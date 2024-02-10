from pydantic import EmailStr
from config.helpers import BaseModelCamel
from merchants.dtos.merchant_dto import MerchantDto

from merchants.models.merchant_user import MerchantUserRole




class MerchantUserCreateODto(BaseModelCamel):
    name: str
    phone: str
    password: str

        

class MerchantUserCreateDto(BaseModelCamel):
    email: EmailStr
    permissions: MerchantUserRole


class MerchantUserDto(BaseModelCamel):
    id: int
    email: EmailStr
    name: str
    permissions: MerchantUserRole
    merchant: MerchantDto



class MerchantUserUpdate(BaseModelCamel):
    email: EmailStr
    name: str
    password: str
