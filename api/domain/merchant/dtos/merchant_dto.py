from datetime import datetime
from typing import Optional

from pydantic import UUID4
from api.config.custom_model import CustomModel
from api.domain.logistic.dtos.address_dto import AddressDto
from api.domain.merchant.models.document_type import DocumentType



class MerchantDto(CustomModel):
    id: Optional[UUID4] = None
    name: str
    corporate_name: str
    description: str
    document_type: DocumentType
    document: str
    created_at: datetime
    address: AddressDto