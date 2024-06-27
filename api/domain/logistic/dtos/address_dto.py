from typing import Optional

from pydantic import UUID4

from api.config.custom_model import CustomModel




class AddressDto(CustomModel):
    id: Optional[UUID4] = None
    street_name: str
    formatted_address: str
    street_number: str
    city: str
    postal_code: str
    neighborhood: str
    state: str
    complement: str 
    latitude: float
    longitude: float
