from datetime import datetime, timedelta, UTC
from typing import Any, Dict, List, Optional
from fastapi import HTTPException, status
from jose import JWTError, jwt
from apps.auth.dtos.auth_dtos import EmailPayloadDTO
from merchants.dtos.merchant_user_admin_dto import MerchantStaffRegistrationDto
from merchants.dtos.merchant_user_dto import MerchantUserDto
from merchants.models.merchant_user import MerchantUser
from config import settings




def create_access_token(user: MerchantUserDto, expires_delta: Optional[timedelta] = None):
    payload: Dict[str, str|int] = user.model_dump()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta 
    else:
        expire = datetime.now(UTC) + timedelta(days=3)
    payload["exp"] =  expire
    encoded_jwt = jwt.encode(payload, settings.TOKEN_SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def create_new_user_email_token(
    admin: MerchantUser, 
    user:  MerchantStaffRegistrationDto, 
    expires_delta: Optional[timedelta] = None):
    
    payload: Dict[str, Any] = {
        "merchant_id": admin.merchant_id,
        "permissions": user.permissions.value,
        "email": user.email
        
    }
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(hours=12)
    payload["exp"] =  expire
    encoded_jwt = jwt.encode(payload, settings.TOKEN_SECRET_KEY, algorithm='HS256')
    return encoded_jwt

def verify_email_token(token: str):
    try:
        payload_dict = jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=['HS256'])
        payload = EmailPayloadDTO(**payload_dict)
        return payload
    except JWTError:
        raise  HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

def verify_token(token: str):
    try:
        payload_dict = jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=['HS256'])
        payload = MerchantUserDto(**payload_dict)
        return payload
    except JWTError:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )