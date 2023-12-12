from pydantic import BaseModel, EmailStr

from restaurants.DTOs.restaurant_dto import RestaurantDTO
from restaurants.models.restaurant_user import Role



class RestaurantUserCreateFromTokenDTO(BaseModel):
    email: EmailStr
    name: str
    phone: str
    password: str
    
    class Config:
        from_attributes = True
        
        

class RestaurantUserCreateTokenDTO(BaseModel):
    email: EmailStr
    permissions: Role

    class Config:
        from_attributes = True


class RestaurantUserDTO(BaseModel):
    id: int
    email: EmailStr
    name: str
    password: str 
    permissions: Role
    restaurant: RestaurantDTO
    
    class Config:
        from_attributes = True



