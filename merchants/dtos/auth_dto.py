from pydantic import BaseModel, ConfigDict, EmailStr
from config.helpers import BaseModelCamel, to_camel
from merchants.dtos.merchant_dto import MerchantDto
from merchants.dtos.merchant_user_dto import MerchantUserDto, MerchantUserPasswordDto



    
class MerchantCreateDto(BaseModelCamel):
    merchant: MerchantDto
    user: MerchantUserPasswordDto
    

class MerchantCreatedOutDTO(BaseModelCamel):
    access_token: str
    merchant_user: MerchantUserDto

class LoginDto(BaseModelCamel):
    email: str
    password: str

class ResponseTokenDto(BaseModelCamel):
    token: str
    merchant_user: MerchantUserDto

class ResponseEmailDto(BaseModelCamel):
    email: EmailStr
    sended: bool
    