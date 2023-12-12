from typing import Literal
from pydantic import BaseModel, EmailStr

from addresses.DTOs.address_dto import AddressCreateDTO, AddressDTO

from enum import Enum

class DocumentType(str, Enum):
    CNPJ = 'cnpj'
    CPF = 'cpf'


class RestaurantUserCreateDTO(BaseModel):
    email: EmailStr
    name: str
    phone:str
    password: str 
    
    class Config:
        from_attributes = True

class RestaurantCreateDTO(BaseModel):
    name: str
    document_type: DocumentType
    document: str
    
    address: AddressCreateDTO
    user: RestaurantUserCreateDTO
    
    class Config:
        from_attributes = True
    

    
class RestaurantUpdateDTO(BaseModel):
    id: int
    name: str
    document_type: DocumentType
    document: str
    
    address: AddressCreateDTO | None
    
    class Config:
        from_attributes = True
    
    
    
    
class RestaurantDTO(BaseModel):
    id: int
    name: str
    document_type: DocumentType
    document: str
    
    address: AddressDTO
    
    class Config:
        from_attributes = True
        
        
class RestaurantCreatedResponseDTO(BaseModel):
    access_token: str
    restaurant: RestaurantDTO
    
    class Config:
        from_attributes = True
