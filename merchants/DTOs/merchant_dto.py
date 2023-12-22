from typing import Literal
from pydantic import BaseModel, EmailStr

from addresses.DTOs.address_dto import AddressCreateDTO, AddressDTO

from enum import Enum



class DocumentType(Enum):
    CNPJ = 'CNPJ'
    CPF = 'CPF'

class MerchantDTO(BaseModel):
    id: int
    name: str
    document_type: DocumentType
    document: str
    
    address: AddressDTO
    
    class Config:
        from_attributes = True

class MerchantUserCreateDTO(BaseModel):
    email: EmailStr
    name: str
    phone:str
    password: str 
    
    class Config:
        from_attributes = True

class MerchantCreateDTO(BaseModel):
    name: str
    document_type: DocumentType
    document: str
    
    address: AddressCreateDTO
    user: MerchantUserCreateDTO
    
    class Config:
        from_attributes = True
    

    
class MerchantUpdateDTO(BaseModel):
    name: str | None
    document_type: DocumentType | None
    document: str | None
    
    address: AddressCreateDTO | None
    
    class Config:
        from_attributes = True
    
        
class MerchantCreatedOutDTO(BaseModel):
    access_token: str
    merchant: MerchantDTO
    
    class Config:
        from_attributes = True