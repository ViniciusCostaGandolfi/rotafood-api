from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from addresses.models.address import Address
from config.authorization.auth import get_current_user
from config.authorization.password_crypt import hash_password
from config.authorization.tokens import create_access_token
from restaurants.DTOs.restaurant_dto import RestaurantCreateDTO, RestaurantCreatedResponseDTO, RestaurantDTO, RestaurantUpdateDTO
from restaurants.models.restaurant import Restaurant
from config.database import get_db
from restaurants.models.restaurant_user import RestaurantUser

restaurant_router = APIRouter(prefix='/restaurants')

class RestaurantController:

    @restaurant_router.get("/all")
    async def get_restaurants(db: Session = Depends(get_db)) -> List[RestaurantDTO]:
        return db.query(Restaurant).all()

    @restaurant_router.get("/")
    async def get_restaurant(
                       db: Session = Depends(get_db), 
                       user: RestaurantUser = Depends(get_current_user)) -> RestaurantDTO:
        restaurant = db.query(Restaurant).filter(Restaurant.id == user.restaurant_id).first()
        
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        return restaurant
    
    @restaurant_router.post("/")
    async def create_restaurant(restaurant_dto: RestaurantCreateDTO, db: Session = Depends(get_db)) -> RestaurantCreatedResponseDTO:
        
        email = db.query(RestaurantUser).filter(RestaurantUser.email == restaurant_dto.user.email).first()
        if email:
            raise HTTPException(status_code=400, detail="E-mail já registrado.")

        
        address_data = restaurant_dto.address.model_dump()
        address = Address(**address_data)
        db.add(address)
        db.commit()
        db.refresh(address) 
        
        restaurant_data = {
            "name": restaurant_dto.name,
            "document_type": restaurant_dto.document_type,
            "document": restaurant_dto.document,
            "address_id": address.id  
        }
        restaurant = Restaurant(**restaurant_data)
        db.add(restaurant)
        db.commit()
        db.refresh(restaurant)


        user_data = restaurant_dto.user.model_dump()
        user_data["restaurant_id"] = restaurant.id
        user_data["password"] = hash_password(user_data["password"])
        user_data["permissions"] = 'OWNER'
        restaurant_user = RestaurantUser(**user_data)
        db.add(restaurant_user)
        db.commit()
        db.refresh(restaurant_user)
        
        restaurant_dto = RestaurantDTO.model_validate(restaurant)
        token = create_access_token(restaurant_user)
        
        return RestaurantCreatedResponseDTO(access_token=token, restaurant=restaurant_dto)


    @restaurant_router.put("/", response_model=RestaurantDTO)
    async def update_restaurant(restaurant_dto: RestaurantUpdateDTO, db: Session = Depends(get_db), user: RestaurantUser = Depends(get_current_user)) -> RestaurantDTO:
        restaurant = db.query(Restaurant).filter(Restaurant.id == user.restaurant_id).first()
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        for key, value in restaurant_dto.model_dump(exclude_unset=True, exclude={'address'}).items():
            setattr(restaurant, key, value)

        if restaurant_dto.address:
            address_data = restaurant_dto.address.model_dump(exclude_unset=True)
            db.query(Address).filter(Address.id == restaurant.address_id).update(address_data)

        db.commit()

        return RestaurantDTO.model_validate(restaurant)