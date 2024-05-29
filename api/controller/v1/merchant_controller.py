from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi_mail import MessageSchema, MessageType
from sqlalchemy.orm import Session
from api.config.pagination import paginate
from api.services.database_service import get_db
from api.services.security.auth_service import get_current_user, permission_dependency
from api.services.security.decode_token_service import create_merchant_user_email_token
from api.domain.merchant.dtos.merchant_dto import MerchantDto
from api.domain.merchant.dtos.merchant_user_dto import MerchantUserDto
from api.domain.merchant.dtos.merchant_user_email_token import MerchantUserEmailTokenDto
from api.domain.merchant.models.merchant import Merchant
from api.domain.merchant.models.merchant_permission import MerchantPermission
from api.domain.merchant.models.merchant_user import MerchantUser
from api.services.email_service import email_sandler

merchant_controller = APIRouter(prefix='/merchants', tags=['Merchant'])


@merchant_controller.get("/")
async def get_merchant(
        merchant_user: MerchantUserDto = Depends(get_current_user),
        db: Session = Depends(get_db)
):

    merchant: Merchant | None = db.query(Merchant).filter(
        Merchant.id == merchant_user.merchant.id).first()
    if merchant:
        return MerchantDto.model_validate(merchant)
    raise HTTPException(401, detail="Restaurante não encontrado")


@merchant_controller.get("/merchant_users/")
async def get_merchant_user_by_merchant(
    merchant_user: MerchantUserDto = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    users = db.query(MerchantUser).filter(
        MerchantUser.merchant_id == merchant_user.merchant.id).all()
    if users:
        users_dto = [MerchantUserDto.model_validate(user) for user in users]
        return paginate(users_dto, 1, 10)

    return HTTPException(401, detail="Usuários não encontrados")


@merchant_controller.get("/merchant_users/{merchant_user_id}")
async def get_merchant_user_by_id(
    merchant_user_id: str,
    merchant_user: MerchantUserDto = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    merchant_user_db: MerchantUser | None = db.query(MerchantUser).filter(
        MerchantUser.merchant_id == merchant_user.merchant.id,
        MerchantUser.id == merchant_user_id).first()
    if merchant_user_db:
        return MerchantUserDto.model_validate(merchant_user_db)
    raise HTTPException(401, detail="Restaurante não encontrado")


@merchant_controller.patch("/")
async def update_merchant(
    merchant_dto: MerchantDto,
    merchant_user: MerchantUserDto = Depends(
        permission_dependency(MerchantPermission.MERCHANT)
    ),
    db: Session = Depends(get_db)
):
    merchant: Merchant | None = db.query(Merchant).filter(
        Merchant.id == merchant_user.merchant.id).first()
    if merchant:
        for key, value in merchant_dto.model_dump(exclude=set(['id', 'address'])).items():
            if hasattr(merchant, key) and value is not None:
                setattr(merchant, key, value)

        if merchant_dto.address:
            address_update_data = merchant_dto.address.model_dump(
                exclude=set(['id']))
            for key, value in address_update_data.items():
                if hasattr(merchant.address, key) and value is not None:
                    setattr(merchant.address, key, value)

        db.commit()

        db.refresh(merchant)

        return MerchantDto.model_validate(merchant)

    raise HTTPException(status_code=404, detail="Comerciante não encontrado")


@merchant_controller.post("/merchant_user/")
async def send_email_for_create_merchant_user(
    create_merchant_user: MerchantUserEmailTokenDto,
    merchant_user_dto: MerchantUserDto = Depends(
        permission_dependency(MerchantPermission.MERCHANT)
    ),
    db: Session = Depends(get_db)
):
    merchant_user: MerchantUser | None = db.query(MerchantUser).filter(
        MerchantUser.email == create_merchant_user.email).first()
    if merchant_user:
        HTTPException(status_code=404, detail="Email já existente")

    create_merchant_user.merchant_id = str(merchant_user_dto.merchant.id)

    token = create_merchant_user_email_token(
        merchant_user_dto, create_merchant_user)

    await email_sandler.send_message(MessageSchema(
        subject=f"RotaFood - {merchant_user_dto.merchant.corporate_name}",
        recipients=[create_merchant_user.email],
        body=f"Por favor, confirme seu registro clicando neste link: https://rotafood.com.br/auth/merchant_user{token}",
        subtype=MessageType.plain
    ))
    return Response(status_code=200)
