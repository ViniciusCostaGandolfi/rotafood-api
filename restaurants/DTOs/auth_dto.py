from pydantic import BaseModel, EmailStr

from restaurants.DTOs.restaurant_user_dto import RestaurantUserDTO


class LoginDTO(BaseModel):
    email: str
    password: str

class ResponseTokenDTO(BaseModel):
    token: str
    restaurant_user: RestaurantUserDTO
    
    class Config:
        from_attributes = True

class ResponseEmailDTO(BaseModel):
    email: EmailStr
    sended: bool