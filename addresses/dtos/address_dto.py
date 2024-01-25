from typing import Optional
from pydantic import BaseModel, ConfigDict



class AddressDto(BaseModel):
    id: Optional[int] = None
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

    model_config = ConfigDict(from_attributes=True)


