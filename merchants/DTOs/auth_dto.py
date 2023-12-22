from pydantic import BaseModel, EmailStr
from merchants.DTOs.merchant_user_dto import MerchantUserOutDTO



class LoginDTO(BaseModel):
    email: str
    password: str

class ResponseTokenDTO(BaseModel):
    token: str
    merchant_user: MerchantUserOutDTO
    
    class Config:
        from_attributes = True

class ResponseEmailDTO(BaseModel):
    email: EmailStr
    sended: bool