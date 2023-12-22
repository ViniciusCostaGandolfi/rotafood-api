from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from addresses.models.address import Address
from config.authorization.auth import get_current_admin_user, get_current_user
from config.database import get_db
from merchants.DTOs.merchant_dto import *
from merchants.models.merchant import Merchant
from merchants.models.merchant_user import MerchantUser

merchant_router = APIRouter(prefix='/merchants')

class RestaurantController:


    @merchant_router.get("/")
    async def get_merchant(
                       db: Session = Depends(get_db), 
                       user: MerchantUser = Depends(get_current_user)) -> MerchantDTO:
        restaurant = db.query(Merchant).filter(Merchant.id == user.merchant_id).first()
        
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        return restaurant


    @merchant_router.put("/", response_model=MerchantDTO)
    async def update_merchant(
        merchant_dto: MerchantUpdateDTO, 
        db: Session = Depends(get_db), 
        user: MerchantUser = Depends(get_current_admin_user)) -> MerchantDTO:
        restaurant = db.query(Merchant).filter(Merchant.id == user.merchant_id).first()
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        for key, value in merchant_dto.model_dump(exclude_unset=True, exclude={'address'}).items():
            setattr(restaurant, key, value)

        if merchant_dto.address:
            address_data = merchant_dto.address.model_dump(exclude_unset=True)
            db.query(Address).filter(Address.id == restaurant.address_id).update(address_data)

        db.commit()

        return MerchantDTO.model_validate(restaurant)