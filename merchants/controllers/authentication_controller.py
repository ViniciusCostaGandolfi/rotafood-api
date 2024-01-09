from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from addresses.models.address import Address
from config.authorization.password_crypt import hash_password, verify_password
from config.authorization.tokens import EmailPayloadDTO, create_access_token, verify_email_token
from config.database import get_db
from merchants.DTOs.auth_dto import *
from merchants.DTOs.merchant_dto import *
from merchants.DTOs.merchant_user_dto import *
from merchants.models.merchant import Merchant
from merchants.models.merchant_user import MerchantUser

authenticaion_router = APIRouter(prefix='/auth')

class MerchantUserAuthController:
    
    @authenticaion_router.post("/merchants/new/")
    async def create_merchant(
        merchant_dto: MerchantCreateDTO, 
        db: Session = Depends(get_db)) -> MerchantCreatedOutDTO:
        
        email = db.query(MerchantUser).filter(MerchantUser.email == merchant_dto.user.email).first()
        if email:
            raise HTTPException(status_code=400, detail="E-mail já registrado.")

        
        address_data = merchant_dto.address.model_dump()
        address = Address(**address_data)
        db.add(address)
        db.commit()
        db.refresh(address) 
        
        merchant_data = {
            "name": merchant_dto.name,
            "document_type": merchant_dto.document_type.value,
            "document": merchant_dto.document,
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
        
        merchant_dto = MerchantDTO.model_validate(merchant)
        token = create_access_token(merchant_user)
        
        return MerchantCreatedOutDTO(access_token=token, merchant=merchant_dto)

    
    @authenticaion_router.post("/merchant_users/login/")
    async def login_merchant_user(
            login_user:LoginDTO,
            db: Session = Depends(get_db)
            ) -> ResponseTokenDTO:
        
        user = db.query(MerchantUser).filter(MerchantUser.email==login_user.email).first()
        if user is not None:
            print(login_user.password, user.password)
            if verify_password(login_user.password, user.password):
                merchant_user_dto = MerchantUserDTO.model_validate(user)
                print(f'\n\n{merchant_user_dto.model_dump}\n\n')
                token_user = create_access_token(user)
                return ResponseTokenDTO(token=token_user, merchant_user=merchant_user_dto)
            
            return HTTPException(401, detail="Senha incorreta")
            
        return HTTPException(401, detail="Email não encontrado")
        
    
    
    @authenticaion_router.post("/merchant_users/new/email/{token}")
    async def create_merchant_user_by_email_token( user_dto: MerchantUserCreateFromTokenDTO,
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
            merchant_user_dto = MerchantUserDTO.model_validate(user)
            token_user = create_access_token(user)
            return ResponseTokenDTO(token=token_user, merchant_user=merchant_user_dto)
        else:
            return HTTPException(401, detail="Email já cadastrado")