from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from addresses.models.address import Address
from config.authorization.auth import get_current_admin_user, get_current_user
from config.database import get_db
from merchants.DTOs.merchant_dto import *
from merchants.models.merchant import Merchant
from merchants.models.merchant_user import MerchantUser
from fastapi import status


merchant_controller = APIRouter(prefix='/merchants')

class RestaurantController:


    @merchant_controller.get("/")
    async def get_merchant(
                       db: Session = Depends(get_db), 
                       user: MerchantUser = Depends(get_current_user)) -> MerchantDTO:
        restaurant = db.query(Merchant).filter(Merchant.id == user.merchant_id).first()
        
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        return restaurant


    @merchant_controller.patch("/", response_model=MerchantDTO)
    async def update_merchant(
        merchant_dto: MerchantUpdateDTO, 
        db: Session = Depends(get_db), 
        user: MerchantUser = Depends(get_current_admin_user)) -> MerchantDTO:
        merchant = db.query(Merchant).filter(Merchant.id == user.merchant_id).first()
        if not merchant:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        
        for key, value in merchant_dto.model_dump(exclude_unset=True, exclude={'address', 'document_type'}).items():
            if value is not None:
                setattr(merchant, key, value)
            
        if merchant_dto.document_type is not None:
            setattr(merchant, 'document_type', merchant_dto.document_type.value)
            
        if merchant_dto.address:
            address_data = merchant_dto.address.model_dump(exclude_unset=True)
            db.query(Address).filter(Address.id == merchant.address_id).update(address_data)

        db.commit()

        return MerchantDTO.model_validate(merchant)
    
    @merchant_controller.delete("/final/delete", response_model={})
    async def delete_merchant(
        db: Session = Depends(get_db), 
        user: MerchantUser = Depends(get_current_admin_user)) -> {}:
        
        merchant = db.query(Merchant).filter(Merchant.id == user.merchant_id).first()
        db.query(MerchantUser).filter(MerchantUser.merchant_id == user.merchant_id).delete()
        db.delete(merchant)
        db.commit()

        return {}