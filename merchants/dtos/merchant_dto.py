from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, EmailStr

from addresses.dtos.address_dto import AddressDto

from enum import Enum

from config.helpers import BaseModelCamel, to_camel


class DocumentType(Enum):
    CNPJ = 'CNPJ'
    CPF = 'CPF'

class MerchantDto(BaseModelCamel):
    id: Optional[int] = None
    name: str
    document_type: DocumentType
    document: str
    address: AddressDto
    

class MerchantUserCreateDto(BaseModelCamel):
    email: EmailStr
    name: str
    phone:str
    password: str 

class MerchantCreateDTO(BaseModelCamel):
    name: str
    document_type: DocumentType
    document: str
    address: AddressDto
    user: MerchantUserCreateDto
    

    
class MerchantUpdateDTO(BaseModelCamel):
    name: str | None
    document_type: DocumentType | None
    document: str | None
    address: AddressDto | None
    
        
class MerchantCreatedOutDTO(BaseModelCamel):
    access_token: str
    merchant: MerchantDto