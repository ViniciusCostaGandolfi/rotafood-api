from datetime import datetime
from typing import Optional
from api.config.custom_model import CustomModel
from api.domain.logistic.dtos.address_dto import AddressDto
from api.domain.merchant.models.document_type import DocumentType
from api.domain.merchant.models.merchant_type import MerchantType



class MerchantDto(CustomModel):
    id: Optional[str] = None
    name: str
    corporate_name: str
    description: str
    document_type: DocumentType
    document: str
    merchant_type: MerchantType
    created_at: datetime
    address: AddressDto