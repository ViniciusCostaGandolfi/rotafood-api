from pydantic import BaseModel, ConfigDict, EmailStr
from merchants.dtos.merchant_user_dto import MerchantUserOutDto



class LoginDTO(BaseModel):
    email: str
    password: str

class ResponseTokenDTO(BaseModel):
    token: str
    merchant_user: MerchantUserOutDto
    
    model_config = ConfigDict(from_attributes=True)

class ResponseEmailDTO(BaseModel):
    email: EmailStr
    sended: bool