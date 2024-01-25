from pydantic import BaseModel, ConfigDict, EmailStr
from merchants.dtos.merchant_user_dto import MerchantUserOutDto



class LoginDto(BaseModel):
    email: str
    password: str

class ResponseTokenDto(BaseModel):
    token: str
    merchant_user: MerchantUserOutDto
    
    model_config = ConfigDict(from_attributes=True)

class ResponseEmailDto(BaseModel):
    email: EmailStr
    sended: bool