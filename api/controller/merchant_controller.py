from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from api.core.authorization.auth import permission_dependency
from api.core.database import get_db
from api.domain.addresses.models.address import Address
from api.domain.merchants.dtos.merchant_dto import MerchantDto, MerchantUpdateDto
from api.domain.merchants.models.merchant import Merchant
from api.domain.merchants.models.merchant_user import MerchantUser, ModulePermissions


merchant_controller = APIRouter(prefix='/merchants', tags=['Merchant'])



@merchant_controller.get("/")
async def get_merchant(
                    db: Session = Depends(get_db), 
                    current_user: MerchantUser = Depends(
                    permission_dependency(ModulePermissions.MERCHANT)
                    )
    ) -> MerchantDto:
    restaurant = db.query(Merchant).filter(Merchant.id == current_user.merchant_id).first()
    
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@merchant_controller.patch("/", response_model=MerchantDto)
async def update_merchant(
    merchant_dto: MerchantUpdateDto, 
    db: Session = Depends(get_db), 
    current_user: MerchantUser = Depends(
        permission_dependency(ModulePermissions.MERCHANT)
        )) -> MerchantDto:
    merchant: Merchant | None = db.query(Merchant).filter(Merchant.id == current_user.merchant_id).first()
    
    
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

    return MerchantDto.model_validate(merchant)

@merchant_controller.delete("/final/delete", status_code=status.HTTP_200_OK)
async def delete_merchant(
    db: Session = Depends(get_db), 
    current_user: MerchantUser = Depends(
        permission_dependency(ModulePermissions.MERCHANT)
        )
    ):
    
    merchant = db.query(Merchant).filter(Merchant.id == current_user.merchant_id).first()
    db.query(MerchantUser).filter(MerchantUser.merchant_id == current_user.merchant_id).delete()
    db.delete(merchant)
    db.commit()

    return Response(status_code=status.HTTP_200_OK)