from pydantic import BaseModel, ConfigDict, EmailStr
from config.helpers import BaseModelCamel, to_camel
from merchants.dtos.merchant_user_dto import MerchantUserOutDto



class LoginDto(BaseModelCamel):
    email: str
    password: str

class ResponseTokenDto(BaseModelCamel):
    token: str
    merchant_user: MerchantUserOutDto

class ResponseEmailDto(BaseModelCamel):
    email: EmailStr
    sended: bool
