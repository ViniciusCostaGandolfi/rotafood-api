from api.config.custom_model import CustomModel
from api.domain.merchant.dtos.merchant_user_email_token import MerchantUserEmailTokenDto

class EmailTokenPayloadDto(CustomModel):
    merchant_user: MerchantUserEmailTokenDto
    exp: float