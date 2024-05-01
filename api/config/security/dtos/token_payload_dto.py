

from api.config.pydantic import CustonModel
from api.domain.merchant.dtos.merchant_user_dto import MerchantUserDto


class TokenPayloadDto(CustonModel):
    merchant_user: MerchantUserDto
    exp: float