from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.config.database import get_db
from api.config.security.auth import get_current_user
from api.config.security.decode_token import verify_merchant_user_email_token
from api.config.security.dtos.email_token_payload_dto import EmailTokenPayloadDto
from api.config.security.decode_token import create_access_token
from api.config.security.password_crypt import hash_password, verify_password
from api.domain.logistic.models.address import Address
from api.domain.merchant.dtos.login_dto import LoginDto
from api.domain.merchant.dtos.merchant_create_dto import MerchantCreateDto
from api.domain.merchant.dtos.merchant_user_create_dto import MerchantUserCreateDto
from api.domain.merchant.dtos.token_dto import TokenDto
from api.domain.merchant.models.merchant import Merchant
from api.domain.merchant.models.merchant_permission import MerchantPermission
from api.domain.merchant.models.merchant_user import MerchantUser

auth_controller = APIRouter(prefix='/auth', tags=['Auth'])

    
@auth_controller.post("/merchants")
async def create_merchant(
    merchant_create_dto: MerchantCreateDto, 
    db: Session = Depends(get_db)) -> TokenDto:
    
    email = db.query(MerchantUser).filter(MerchantUser.email == merchant_create_dto.owner.email).first()
    if email:
        raise HTTPException(status_code=400, detail="E-mail já registrado.")

    address = Address(**merchant_create_dto.merchant.address.model_dump())
    db.add(address)
    db.commit()
    db.refresh(address) 
    
    
    merchant = Merchant(
        **merchant_create_dto.merchant.model_dump(exclude=set('address')),
            address_id=address.id
        )
    db.add(merchant) 
    db.commit()
    db.refresh(merchant)


    merchant_user = MerchantUser(
        name = merchant_create_dto.owner.name,
        email = merchant_create_dto.owner.email,
        password = hash_password(merchant_create_dto.owner.password),
        phone = merchant_create_dto.owner.phone,
        permissions = [permission.value for permission in MerchantPermission],
        merchant_id = merchant.id,
    )
    db.add(merchant_user)
    db.commit()
    db.refresh(merchant_user)
    
    token = create_access_token(merchant_user)
    
    return TokenDto(token=token)


@auth_controller.post("/login/")
async def login_merchant_user(
        login_dto:LoginDto,
        db: Session = Depends(get_db)
        ) -> TokenDto:
    
    user:MerchantUser | None  = db.query(MerchantUser).filter(MerchantUser.email==login_dto.email).first()
    if user:
        if verify_password(login_dto.password, str(user.password)):
            token_user = create_access_token(user)
            return TokenDto(token=token_user)
        raise HTTPException(401, detail="Credenciais inválidas")
    raise HTTPException(401, detail="Email não encontrado")
    


@auth_controller.post("/merchant_users/{token}/")
async def create_merchant_user_by_email_token( 
                user_create_dto: MerchantUserCreateDto,
                payload: EmailTokenPayloadDto = Depends(verify_merchant_user_email_token), 
                db: Session = Depends(get_db)
                ):
    
    email = db.query(MerchantUser).filter(MerchantUser.email==payload.email).first()
    if email is None:
        user = MerchantUser(
            name=user_create_dto.name,
            password=hash_password(user_create_dto.password),
            phone = user_create_dto.phone,
            email=payload.email,
            permissions=[permission.value for permission in payload.permissions],
            merchant_id=payload.merchant_id)
        
        db.add(user)
        db.commit()
        db.refresh(user)
        return TokenDto(token=create_access_token(user))
    else:
        return HTTPException(401, detail="Email já cadastrado")
    
@auth_controller.post("/refresh_token/")
async def refresh_token( 
                current_user = Depends(get_current_user), 
                ):
    return TokenDto(token=create_access_token(current_user))

    
