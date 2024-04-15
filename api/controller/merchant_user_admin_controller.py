from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi_mail import MessageSchema
from fastapi import status
from sqlalchemy.orm import Session
from api.core.authorization.auth import get_current_user, has_permission, permission_dependency
from api.core.authorization.tokens import create_new_user_email_token
from api.core.database import get_db
from api.core.email import email_sandler
from api.domain.merchants.dtos.merchant_user_admin_dto import MerchantStaffRegistrationDto
from api.domain.merchants.dtos.merchant_user_dto import MerchantUserDto
from api.domain.merchants.models.merchant import Merchant
from api.domain.merchants.models.merchant_user import MerchantUser, ModulePermissions


merchant_user_admin_controller = APIRouter(prefix='/merchant_users', tags=['MerchantUserAdmin'])

    
@merchant_user_admin_controller.post("/new/email/", status_code=status.HTTP_200_OK)
async def send_email_create_MerchantUser(
    user_dto: MerchantStaffRegistrationDto, 
    current_user: MerchantUser = Depends(get_current_user)) -> MerchantStaffRegistrationDto:
    
    
    if not has_permission(current_user, ModulePermissions.MERCHANT):
        return HTTPException(status_code=403, detail="Acesso Negado")
        
    token = create_new_user_email_token(current_user, user_dto)
    link = f'https://rotafood.com.br/accounts/merchant_user/new/email/{token}'
    
    message = MessageSchema(
        subject='Crie sua conta agora!',
        recipients=[user_dto.email],
        body=f'Crie sua conta agora no {current_user.merchant.name} \n\n\n acessando o link: {link}',
        subtype='plain'
    )
    
    await email_sandler.send_message(message)
    return Response(status_code=status.HTTP_200_OK)

@merchant_user_admin_controller.put("/{merchant_user_id}", response_model=MerchantUserDto)
async def update_merchant_user_by_id(
    merchant_id: int, 
    merchant_user_data: MerchantUserDto, 
    db: Session = Depends(get_db),
    current_user: MerchantUser = Depends(
                    permission_dependency(ModulePermissions.MERCHANT)
                    )
    ) -> MerchantUser:
    

    
    merchant_user_db = db.query(Merchant).filter(Merchant.id == merchant_id, merchant_id=current_user.merchant_id).first()
    if not merchant_user_db:
        raise HTTPException(status_code=404, detail="Restaurante não encontrado")

    for key, value in merchant_user_data.model_dump(exclude={"permissions"}).items():
        if value is not None:
            setattr(merchant_user_db, key, value)
    
    if merchant_user_data.permissions is not None:
        setattr(merchant_user_db, "permissions", merchant_user_data.permissions)
    
    db.commit()

    return MerchantUserDto.model_validate(merchant_user_db)


@merchant_user_admin_controller.delete("/{merchant_user_id}", status_code=status.HTTP_200_OK)
async def delete_merchant_user_by_id(
    merchant_user_id: int, 
    db: Session = Depends(get_db),
    current_user: MerchantUser = Depends(
                    permission_dependency(ModulePermissions.MERCHANT)
                    )
    ):
    
    merchant_user = db.query(MerchantUser).filter(MerchantUser.id == merchant_user_id, merchant_id=current_user.merchant_id).first()
    if not merchant_user:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    db.delete(merchant_user)
    db.commit()
    
    return Response(status_code=status.HTTP_200_OK)

