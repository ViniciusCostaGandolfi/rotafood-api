from api.config.custom_model import CustomModel


class MerchantUserCreateDto(CustomModel):
    name: str
    phone: str
    password: str