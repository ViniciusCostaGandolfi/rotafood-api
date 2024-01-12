from pydantic import BaseModel, ConfigDict, EmailStr
from merchants.DTOs.merchant_dto import MerchantDTO

from merchants.models.merchant_user import MerchantUserRole




class MerchantUserCreateFromTokenDTO(BaseModel):
    name: str
    phone: str
    password: str
    
    model_config = ConfigDict(from_attributes=True)
        

class MerchantUserCreateTokenDTO(BaseModel):
    email: EmailStr
    permissions: MerchantUserRole

    model_config = ConfigDict(from_attributes=True)


class MerchantUserDTO(BaseModel):
    id: int
    email: EmailStr
    name: str
    password: str 
    permissions: MerchantUserRole
    merchant: MerchantDTO
    
    model_config = ConfigDict(from_attributes=True)
class MerchantUserOutDTO(BaseModel):
    id: int
    email: EmailStr
    name: str
    permissions: MerchantUserRole
    merchant: MerchantDTO
    
    model_config = ConfigDict(from_attributes=True)


class MerchantUserUpdate(BaseModel):
    email: EmailStr
    name: str
    password: str
