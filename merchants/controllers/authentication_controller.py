from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from addresses.dtos.address_dto import AddressDto
from addresses.models.address import Address
from config.authorization.password_crypt import hash_password, verify_password
from config.authorization.tokens import EmailPayloadDTO, create_access_token, verify_email_token
from config.database import get_db
from merchants.dtos.auth_dto import *
from merchants.dtos.merchant_user_dto import *
from merchants.models.merchant import Merchant
from merchants.models.merchant_user import MerchantUser

authenticaion_controller = APIRouter(prefix='/auth', tags=['Auth'])

    
@authenticaion_controller.post("/merchants/create/")
async def create_merchant(
    merchant_dto: MerchantCreateDto, 
    db: Session = Depends(get_db)) -> MerchantCreatedOutDTO:
    
    email = db.query(MerchantUser).filter(MerchantUser.email == merchant_dto.user.email).first()
    if email:
        raise HTTPException(status_code=400, detail="E-mail já registrado.")

    
    address_data: AddressDto = merchant_dto.merchant.address.model_dump()
    address = Address(**address_data)
    db.add(address)
    db.commit()
    db.refresh(address) 
    
    merchant_data = {
        "name": merchant_dto.merchant.name,
        "document_type": merchant_dto.merchant.document_type.value,
        "document": merchant_dto.merchant.document,
        "address_id": address.id  
    }
    merchant = Merchant(**merchant_data)
    db.add(merchant)
    db.commit()
    db.refresh(merchant)


    user_data = merchant_dto.user.model_dump()
    user_data["merchant_id"] = merchant.id
    user_data["password"] = hash_password(user_data["password"])
    user_data["permissions"] = MerchantUserRole.OWNER.value
    merchant_user = MerchantUser(**user_data)
    db.add(merchant_user)
    db.commit()
    db.refresh(merchant_user)
    
    token = create_access_token(merchant_user)
    merchant_user_dto = MerchantUserDto.model_validate(merchant_user)
    
    return MerchantCreatedOutDTO(access_token=token, merchant_user=merchant_user_dto)


@authenticaion_controller.post("/merchant_users/login/")
async def login_merchant_user(
        login_user:LoginDto,
        db: Session = Depends(get_db)
        ) -> ResponseTokenDto:
    
    user = db.query(MerchantUser).filter(MerchantUser.email==login_user.email).first()
    if user is not None:
        print(login_user.password, user.password)
        if verify_password(login_user.password, user.password):
            merchant_user_dto = MerchantUserDto.model_validate(user)
            print(f'\n\n{merchant_user_dto.model_dump}\n\n')
            token_user = create_access_token(user)
            return ResponseTokenDto(token=token_user, merchant_user=merchant_user_dto)
        
        return HTTPException(401, detail="Senha incorreta")
        
    return HTTPException(401, detail="Email não encontrado")
    


@authenticaion_controller.post("/merchant_users/email/{token}/")
async def create_merchant_user_by_email_token( user_dto: MerchantUserCreateFromTokenDto,
                payload: EmailPayloadDTO = Depends(verify_email_token), 
                db: Session = Depends(get_db)):
    
    email = db.query(MerchantUser).filter(MerchantUser.email==payload.email).first()
    if email is None:
        user = MerchantUser(**user_dto.model_dump(), 
                                email=payload.email,
                                merchant_id=payload.merchant_id, 
                                permissions=payload.permissions.value)
        print(user_dto, user)
        db.add(user)
        db.commit()
        db.refresh(user)
        merchant_user_dto = MerchantUserDto.model_validate(user)
        token_user = create_access_token(user)
        return ResponseTokenDto(token=token_user, merchant_user=merchant_user_dto)
    else:
        return HTTPException(401, detail="Email já cadastrado")
    
# @authenticaion_controller.get("/get_token_ifood")
# async def get_token_ifood():
#     token = await get_rotafood_acess_token()

#     return token