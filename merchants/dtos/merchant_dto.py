from typing import Optional
from pydantic import EmailStr

from addresses.dtos.address_dto import AddressDto

from enum import Enum

from config.helpers import BaseModelCamel


class DocumentType(Enum):
    CNPJ = 'CNPJ'
    CPF = 'CPF'

class MerchantDto(BaseModelCamel):
    id: Optional[int] = None
    name: str
    document_type: DocumentType
    document: str
    address: AddressDto
    
    
class MerchantUpdateDto(BaseModelCamel):
    name: str | None
    document_type: DocumentType | None
    document: str | None
    address: AddressDto | None
    
        