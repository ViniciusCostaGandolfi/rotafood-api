from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, EmailStr

from addresses.dtos.address_dto import AddressDto

from enum import Enum



class DocumentType(Enum):
    CNPJ = 'CNPJ'
    CPF = 'CPF'

class MerchantDto(BaseModel):
    id: Optional[int] = None
    name: str
    document_type: DocumentType
    document: str
    
    address: AddressDto
    
    model_config = ConfigDict(from_attributes=True)

class MerchantUserCreateDto(BaseModel):
    email: EmailStr
    name: str
    phone:str
    password: str 
    
    model_config = ConfigDict(from_attributes=True)

class MerchantCreateDTO(BaseModel):
    name: str
    document_type: DocumentType
    document: str
    
    address: AddressDto
    user: MerchantUserCreateDto
    
    model_config = ConfigDict(from_attributes=True)
    

    
class MerchantUpdateDTO(BaseModel):
    name: str | None
    document_type: DocumentType | None
    document: str | None
    
    address: AddressDto | None
    
    model_config = ConfigDict(from_attributes=True)
    
        
class MerchantCreatedOutDTO(BaseModel):
    access_token: str
    merchant: MerchantDto
    
    model_config = ConfigDict(from_attributes=True)