from typing import Optional
from pydantic import EmailStr
from api.config.pydantic import CustonModel
from api.domain.logistic.dtos.address_dto import AddressDto
from api.domain.merchant.models.merchant_type import MerchantType



class MerchantDto(CustonModel):
    id: Optional[str] = None
    name: str
    corporate_name: str
    description: str
    document: str
    merchant_type: MerchantType
    created_at: str
    address: AddressDto