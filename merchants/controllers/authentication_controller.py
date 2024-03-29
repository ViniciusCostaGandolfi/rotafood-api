from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from addresses.dtos.address_dto import AddressDto
from addresses.models.address import Address
from config.authorization.auth import get_current_user
from config.authorization.password_crypt import hash_password, verify_password
from config.authorization.tokens import EmailPayloadDTO, create_access_token, verify_email_token
from config.database import get_db
from merchants.dtos.auth_dto import AuthTokenDto, MerchantRegistrationDto, UserLoginDto, UserRegistrationDto
from merchants.models.merchant import Merchant
from merchants.models.merchant_user import MerchantUser, ModulePermissions

authenticaion_controller = APIRouter(prefix='/auth', tags=['Auth'])

    
@authenticaion_controller.post("/merchants/create/")
async def create_merchant(
    merchant_dto: MerchantRegistrationDto, 
    db: Session = Depends(get_db)) -> AuthTokenDto:
    
    email = db.query(MerchantUser).filter(MerchantUser.email == merchant_dto.user.email).first()
    if email:
        raise HTTPException(status_code=400, detail="E-mail já registrado.")

    
    address_data: AddressDto = merchant_dto.merchant.address.model_dump()
    address = Address(**address_data)
    db.add(address)
    db.commit()
    db.refresh(address) 
    
    
    merchant = Merchant(
        **merchant_dto.merchant.model_dump(exclude=['address']),
            address_id=address.id
        )
    db.add(merchant) 
    db.commit()
    db.refresh(merchant)


    user_data = merchant_dto.user.model_dump()
    user_data["merchant_id"] = merchant.id
    user_data["password"] = hash_password(user_data["password"])
    user_data["permissions"] = [
        ModulePermissions.MERCHANT.value,
        ModulePermissions.COMMANDS.value,
        ModulePermissions.DRIVERS.value,
        ModulePermissions.ORDERS.value,
        ModulePermissions.ROUTES.value,
        ModulePermissions.INTEGRATION.value,
        ModulePermissions.PRODUCTS.value,
        ModulePermissions.CATALOGS.value
    ]
    merchant_user = MerchantUser(**user_data)
    db.add(merchant_user)
    db.commit()
    db.refresh(merchant_user)
    
    token = create_access_token(merchant_user)
    
    return AuthTokenDto(access_token=token)


@authenticaion_controller.post("/merchant_users/login/")
async def login_merchant_user(
        login_user:UserLoginDto,
        db: Session = Depends(get_db)
        ) -> AuthTokenDto:
    
    user: MerchantUser | None = db.query(MerchantUser).filter(MerchantUser.email==login_user.email).first()
    if user is not None:
        print('USER EMAIL', user.email)
        if verify_password(login_user.password, user.password):
            token_user = create_access_token(user)
            return AuthTokenDto(access_token=token_user)
        
        raise HTTPException(401, detail="Senha incorreta")
        
    raise HTTPException(401, detail="Email não encontrado")
    


@authenticaion_controller.post("/merchant_users/email/{token}/")
async def create_merchant_user_by_email_token( 
                user_dto: UserRegistrationDto,
                payload: EmailPayloadDTO = Depends(verify_email_token), 
                db: Session = Depends(get_db)
                ):
    
    email = db.query(MerchantUser).filter(MerchantUser.email==payload.email).first()
    if email is None:
        user = MerchantUser(**user_dto.model_dump(), 
                                email=payload.email,
                                merchant_id=payload.merchant_id, 
                                permissions=payload.permissions.value)
        db.add(user)
        db.commit()
        db.refresh(user)
        token_user = create_access_token(user)
        return AuthTokenDto(access_token=token_user)
    else:
        return HTTPException(401, detail="Email já cadastrado")
    
@authenticaion_controller.post("/refresh_token/")
async def refresh_token( 
                current_user = Depends(get_current_user), 
                ):
    
    
    token_user = create_access_token(current_user)
    return AuthTokenDto(access_token=token_user)

    
