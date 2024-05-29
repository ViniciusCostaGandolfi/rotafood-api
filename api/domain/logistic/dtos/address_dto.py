from typing import Optional

from api.config.custom_model import CustomModel




class AddressDto(CustomModel):
    id: Optional[str] = None
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
