from pydantic import BaseModel, constr, conint, confloat


class AddressDTO(BaseModel):
    id: int
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

    class Config:
        from_attributes = True


class AddressCreateDTO(BaseModel):
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

    class Config:
        from_attributes = True
