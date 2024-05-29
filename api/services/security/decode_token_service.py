from datetime import UTC, datetime, timedelta
from typing import Any, Dict, List, Optional
from fastapi import HTTPException, status
from jose import JWTError, jwt
from api.config.env_settings import settings
from api.services.security.dtos.email_token_payload_dto import EmailTokenPayloadDto
from api.services.security.dtos.token_payload_dto import TokenPayloadDto
from api.domain.merchant.dtos.merchant_user_dto import MerchantUserDto
from api.domain.merchant.dtos.merchant_user_email_token import MerchantUserEmailTokenDto
from api.domain.merchant.models.merchant_user import MerchantUser


SECRET_KEY = settings.TOKEN_SECRET_KEY
ALGORITHM = "HS256"

def create_access_token(merchant_user: MerchantUserDto, expires_delta: Optional[timedelta] = None):
    
    expire = datetime.now(UTC) + timedelta(days=3)
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta         
    
    return jwt.encode(
        TokenPayloadDto(
            merchant_user=merchant_user, 
            exp=expire.timestamp()
            ).model_dump(), SECRET_KEY, algorithm=ALGORITHM)

def create_merchant_user_email_token(
    admin: MerchantUserDto, 
    user:  MerchantUserEmailTokenDto, 
    expires_delta: Optional[timedelta] = None) -> str:

    expire = datetime.now(UTC) + timedelta(days=7)
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta  
        
    return jwt.encode(EmailTokenPayloadDto(
            merchant_user=MerchantUserEmailTokenDto(
                merchant_id=str(admin.merchant.id),
                permissions=user.permissions,
                email=user.email
            ),
            exp=expire.timestamp()
        ).model_dump(), SECRET_KEY, algorithm=ALGORITHM)

def verify_merchant_user_email_token(token: str) -> MerchantUserEmailTokenDto:
    try:
        payload_dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return MerchantUserEmailTokenDto(**payload_dict)
    
    except JWTError:
        raise  HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

def verify_token(token: str) -> MerchantUserDto:
    try:
        payload_dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return MerchantUserDto(**payload_dict)
    except JWTError:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )




