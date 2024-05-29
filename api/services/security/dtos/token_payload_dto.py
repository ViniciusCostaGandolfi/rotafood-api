from api.config.custom_model import CustomModel
from api.domain.merchant.dtos.merchant_user_dto import MerchantUserDto


class TokenPayloadDto(CustomModel):
    merchant_user: MerchantUserDto
    exp: float