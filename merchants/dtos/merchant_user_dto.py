from typing import List
from pydantic import EmailStr
from config.helpers import BaseModelCamel
from merchants.dtos.merchant_dto import MerchantDto

from merchants.models.merchant_user import ModulePermissions




class MerchantUserCreateODto(BaseModelCamel):
    name: str
    phone: str
    password: str

        

class MerchantUserCreateDto(BaseModelCamel):
    email: EmailStr
    permissions: List[ModulePermissions]


class MerchantUserDto(BaseModelCamel):
    id: int
    email: EmailStr
    name: str
    permissions: List[ModulePermissions]
    merchant: MerchantDto



class MerchantUserUpdate(BaseModelCamel):
    email: EmailStr
    name: str
    password: str
