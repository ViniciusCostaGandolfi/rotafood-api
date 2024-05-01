from api.config.pydantic import CustonModel


class MerchantUserCreateDto(CustonModel):
    name: str
    phone: str
    password: str