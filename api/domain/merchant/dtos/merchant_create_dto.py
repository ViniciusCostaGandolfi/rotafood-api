from pydantic import EmailStr
from api.config.pydantic import CustonModel
from api.domain.merchant.dtos.merchant_dto import MerchantDto

class OwnerDto(CustonModel):
    name: str
    email: EmailStr
    phone: str
    password: str

class MerchantCreateDto(CustonModel):
    merchant: MerchantDto
    owner: OwnerDto




