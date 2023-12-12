from fastapi import APIRouter, Depends, HTTPException
from fastapi_mail import MessageSchema
from sqlalchemy.orm import Session
from typing import Any, List
from config.authorization.auth import get_current_admin_user, get_current_user
from config.authorization.tokens import EmailPayloadDTO, create_new_user_email_token, verify_email_token
from restaurants.DTOs.auth_dto import ResponseEmailDTO, ResponseTokenDTO
from restaurants.DTOs.restaurant_user_dto import RestaurantUserCreateFromTokenDTO, RestaurantUserCreateTokenDTO, RestaurantUserDTO
from restaurants.models.restaurant import Restaurant
from config.database import get_db
from restaurants.models.restaurant_user import RestaurantUser
from config.email import email_sandler

restaurant_user_router = APIRouter(prefix='/restaurant_users')

class RestaurantUserController:

    @restaurant_user_router.get("/all/", response_model=List[RestaurantUserDTO])
    async def get_all(
            db: Session = Depends(get_db), 
            user: RestaurantUser = Depends(get_current_user)) -> List[RestaurantUser]:
        users =  db.query(RestaurantUser).filter(RestaurantUser.restaurant_id == user.restaurant_id).all()

        if not users:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        
        return users
    
    @restaurant_user_router.get("/{restaurant_user_id}", response_model=RestaurantUserDTO)
    async def get(restaurant_user_id:int,
            db: Session = Depends(get_db), 
            current_user: RestaurantUser = Depends(get_current_user)) -> RestaurantUser:
        
        if restaurant_user_id:
            user =  db.query(RestaurantUser).filter(RestaurantUser.restaurant_id == restaurant_user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            return user
        
        return current_user

    @restaurant_user_router.post("/new/email/", response_model=ResponseEmailDTO)
    async def post(user_dto: RestaurantUserCreateTokenDTO, 
             admin: RestaurantUser = Depends(get_current_admin_user)) -> ResponseEmailDTO:
        
        
        token = create_new_user_email_token(admin, user_dto)
        link = f'https://rotafood.com.br/accounts/restaurant_user/new/email/{token}'
        
        message = MessageSchema(
            subject='Crie sua conta agora!',
            recipients=[user_dto.email],
            body=f'Crie sua conta agora no {admin.restaurant.name} \n\n\n acessando o link: {link}',
            subtype='plain'
        )
        
        await email_sandler.send_message(message)
        return ResponseEmailDTO(email=user_dto.email, sended=True)
    
    @restaurant_user_router.post("/new/email/{token}")
    async def post( user_dto: RestaurantUserCreateFromTokenDTO,
                    payload: EmailPayloadDTO = Depends(verify_email_token), 
                    db: Session = Depends(get_db)):
        
        email = db.query(RestaurantUser).filter(RestaurantUser.email==payload.email).first()
        print("email", email, type(email))
        if email is None:
            user = RestaurantUser(**user_dto.model_dump(), 
                                    restaurant_id=payload.restaurant_id, 
                                    permissions=payload.permissions)
            db.add(user)
            db.commit()
            db.refresh(user)
            return RestaurantUserDTO.model_validate(user)
        else:
            return HTTPException(401, detail="Email já cadastrado")
    
    # @restaurant_user_router.post("/login/", response_model=ResponseTokenDTO)
    # async def login(
    #     user_dto: RestaurantUserCreateDTO, 
    #     db: Session = Depends(get_db),
    #     admin: RestaurantUser = Depends(get_current_admin_user)) -> ResponseTokenDTO:

    #     restaurant_user = RestaurantUser(**user_dto.model_dump(), restaurant_id=admin.restaurant_id)
    #     db.add(restaurant_user)
    #     db.commit()
    #     db.refresh(restaurant_user)
    #     return RestaurantUserDTO(**restaurant_user)



    @restaurant_user_router.put("/", response_model=RestaurantUserDTO)
    async def update(restaurant_id: int, restaurant_data: RestaurantUserDTO, db: Session = Depends(get_db)) -> RestaurantUser:
        restaurant_user = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

        
        if not restaurant_user:
            raise HTTPException(status_code=404, detail="Restaurante não encontrado")

        for key, value in restaurant_data.model_dump().items():
            setattr(restaurant_user, key, value)
      
        db.commit()

        return restaurant_user
    

    @restaurant_user_router.delete("/{restaurant_user_id}", response_model=dict)
    async def delete(restaurant_user_id: int, db: Session = Depends(get_db), user:RestaurantUser = Depends(get_current_admin_user)):
        
        restaurant_user = db.query(RestaurantUser).filter(RestaurantUser.id == restaurant_user_id).first()
        if not restaurant_user:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        db.delete(restaurant_user)
        db.commit()
        return {"ok": True}