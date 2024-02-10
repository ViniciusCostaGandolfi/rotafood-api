from pydantic import EmailStr
from config.helpers import BaseModelCamel
from merchants.dtos.merchant_dto import MerchantDto

class UserRegistrationDto(BaseModelCamel):
    name: str
    email: EmailStr
    phone: str
    password: str

class MerchantRegistrationDto(BaseModelCamel):
    merchant: MerchantDto 
    user: UserRegistrationDto

class AuthTokenDto(BaseModelCamel):
    access_token: str

class UserLoginDto(BaseModelCamel):
    email: str
    password: str
