from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.core.authorization.auth import get_current_user
from api.core.database import get_db
from api.domain.merchants.dtos.merchant_user_dto import MerchantUserDto, MerchantUserUpdate
from api.domain.merchants.models.merchant_user import MerchantUser

merchant_user_controller = APIRouter(prefix='/merchant_users', tags=['MerchantUser'])

@merchant_user_controller.get("/", response_model=MerchantUserDto)
async def get_MerhantUser(
        current_user: MerchantUser = Depends(get_current_user)
        ) -> MerchantUser:
    return MerchantUserDto.model_validate(current_user)

@merchant_user_controller.get("/{merchant_user_id}", response_model=MerchantUserDto)
async def get_merchant_user_by_id(
        merchant_user_id:int,
        db: Session = Depends(get_db), 
        current_user: MerchantUser = Depends(get_current_user)) -> MerchantUser:
    
    user =  db.query(MerchantUser).filter(MerchantUser.merchant_id == merchant_user_id, merchant_id=current_user.merchant_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return MerchantUserDto.model_validate(user)

@merchant_user_controller.get("/all/", response_model=List[MerchantUserDto])
async def get_all_merchant_users(
        db: Session = Depends(get_db), 
        user: MerchantUser = Depends(get_current_user)) -> List[MerchantUser]:
    users =  db.query(MerchantUser).filter(MerchantUser.merchant_id == user.merchant_id).all()
    if not users:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return users


@merchant_user_controller.put("/", response_model=MerchantUserDto)
async def update_merchant_user(
        merchant_user_data:MerchantUserUpdate,
        current_user: MerchantUser = Depends(get_current_user),
        db: Session = Depends(get_db)) -> MerchantUser:
    
    for key, value in merchant_user_data.model_dump().items():
        setattr(current_user, key, value)
    
    db.commit()
    
    return MerchantUserDto.model_validate(current_user)
