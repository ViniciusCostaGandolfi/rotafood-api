from pydantic import BaseModel, constr, conint, confloat


class AddressDTO(BaseModel):
    id: int
    number: str | None
    street: str
    neighborhood: str | None
    city: str
    state: str
    postal_code: str
    lat: float
    lon: float

    class Config:
        from_attributes = True


class AddressCreateDTO(BaseModel):
    number: str | None
    street: str
    neighborhood: str | None
    city: str
    state: str
    postal_code: str
    lat: float
    lon: float

    class Config:
        from_attributes = True
