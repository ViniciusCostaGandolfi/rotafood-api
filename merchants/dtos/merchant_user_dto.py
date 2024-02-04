from pydantic import BaseModel, ConfigDict, EmailStr
from config.helpers import BaseModelCamel, to_camel
from merchants.dtos.merchant_dto import MerchantDto

from merchants.models.merchant_user import MerchantUserRole




class MerchantUserCreateFromTokenDto(BaseModelCamel):
    name: str
    phone: str
    password: str

        

class MerchantUserCreateTokenDto(BaseModelCamel):
    email: EmailStr
    permissions: MerchantUserRole


class MerchantUserDto(BaseModelCamel):
    id: int
    email: EmailStr
    name: str
    password: str 
    permissions: MerchantUserRole
    merchant: MerchantDto

class MerchantUserOutDto(BaseModelCamel):
    id: int
    email: EmailStr
    name: str
    permissions: MerchantUserRole
    merchant: MerchantDto



class MerchantUserUpdate(BaseModelCamel):
    email: EmailStr
    name: str
    password: str
