from fastapi import APIRouter, Depends, HTTPException
from fastapi_mail import MessageSchema
from sqlalchemy.orm import Session
from config.authorization.auth import get_current_admin_user
from config.authorization.tokens import create_new_user_email_token
from config.database import get_db
from config.email import email_sandler
from merchants.DTOs.auth_dto import *
from merchants.DTOs.merchant_user_dto import *
from merchants.models.merchant import Merchant
from merchants.models.merchant_user import MerchantUser

merchant_user_admin_controller = APIRouter(prefix='/merchant_users')

    
@merchant_user_admin_controller.post("/new/email/", response_model=ResponseEmailDTO)
async def send_email_create_MerchantUser(
    user_dto: MerchantUserCreateTokenDTO, 
    admin: MerchantUser = Depends(get_current_admin_user)) -> ResponseEmailDTO:
    
    
    token = create_new_user_email_token(admin, user_dto)
    link = f'https://rotafood.com.br/accounts/merchant_user/new/email/{token}'
    
    message = MessageSchema(
        subject='Crie sua conta agora!',
        recipients=[user_dto.email],
        body=f'Crie sua conta agora no {admin.merchant.name} \n\n\n acessando o link: {link}',
        subtype='plain'
    )
    
    await email_sandler.send_message(message)
    return ResponseEmailDTO(email=user_dto.email, sended=True)

@merchant_user_admin_controller.put("/{merchant_user_id}", response_model=MerchantUserDTO)
async def update_merchant_user_by_id(
    merchant_id: int, 
    merchant_user_data: MerchantUserDTO, 
    admin:MerchantUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)) -> MerchantUser:
    
    
    merchant_user = db.query(Merchant).filter(Merchant.id == merchant_id, merchant_id=admin.merchant_id).first()
    if not merchant_user:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")

    for key, value in merchant_user_data.model_dump(exclude={"permissions"}).items():
        if value is not None:
            setattr(merchant_user, key, value)
    
    if merchant_user_data.permissions.value is not None:
        setattr(merchant_user, "permissions", merchant_user_data.permissions.value)
    
    db.commit()

    return merchant_user


@merchant_user_admin_controller.delete("/{merchant_user_id}", response_model=dict)
async def delete_merchant_user_by_id(
    merchant_user_id: int, 
    admin:MerchantUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)):
    
    merchant_user = db.query(MerchantUser).filter(MerchantUser.id == merchant_user_id, merchant_id=admin.merchant_id).first()
    if not merchant_user:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    db.delete(merchant_user)
    db.commit()
    return {"ok": True}

