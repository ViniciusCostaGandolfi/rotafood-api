from pydantic import BaseModel, EmailStr
from merchants.DTOs.merchant_dto import MerchantDTO

from merchants.models.merchant_user import MerchantUserRole




class MerchantUserCreateFromTokenDTO(BaseModel):
    name: str
    phone: str
    password: str
    
    class Config:
        from_attributes = True
        
        

class MerchantUserCreateTokenDTO(BaseModel):
    email: EmailStr
    permissions: MerchantUserRole

    class Config:
        from_attributes = True


class MerchantUserDTO(BaseModel):
    id: int
    email: EmailStr
    name: str
    password: str 
    permissions: MerchantUserRole
    merchant: MerchantDTO
    
    class Config:
        from_attributes = True
        
class MerchantUserOutDTO(BaseModel):
    id: int
    email: EmailStr
    name: str
    permissions: MerchantUserRole
    merchant: MerchantDTO
    
    class Config:
        from_attributes = True


class MerchantUserUpdate(BaseModel):
    email: EmailStr
    name: str
    password: str
