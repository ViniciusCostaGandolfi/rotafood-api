from pydantic import EmailStr
from api.config.custom_model import CustomModel
from api.domain.logistic.dtos.address_dto import AddressDto
from api.domain.merchant.models.document_type import DocumentType
from api.domain.merchant.models.merchant_type import MerchantType

class OwnerDto(CustomModel):
    name: str
    email: EmailStr
    phone: str
    password: str
    
class MerchantDto(CustomModel):
    name: str
    corporate_name: str
    description: str
    document_type: DocumentType
    document: str
    address: AddressDto

class MerchantCreateDto(CustomModel):
    merchant: MerchantDto
    owner: OwnerDto




