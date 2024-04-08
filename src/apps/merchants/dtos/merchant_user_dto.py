from typing import List

from pydantic import EmailStr
from custom_model import CustomModel

from merchants.dtos.merchant_dto import MerchantDto

from merchants.models.merchant_user import ModulePermissions




class MerchantUserCreateODto(CustomModel):
    name: str
    phone: str
    password: str

        

class MerchantUserCreateDto(CustomModel):
    email: EmailStr
    permissions: List[ModulePermissions]


class MerchantUserDto(CustomModel):
    id: int
    email: EmailStr
    name: str
    permissions: List[ModulePermissions]
    merchant: MerchantDto



class MerchantUserUpdate(CustomModel):
    email: EmailStr
    name: str
    password: str
