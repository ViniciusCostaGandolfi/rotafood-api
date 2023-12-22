from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from fastapi import HTTPException, status
from jose import JWTError, jwt
from pydantic import BaseModel
from merchants.DTOs.merchant_user_dto import MerchantUserCreateTokenDTO
from merchants.models.merchant_user import MerchantUser, MerchantUserRole
from dotenv import load_dotenv
import os

load_dotenv()


SECRET_KEY = os.environ.get("SECRET_KEY", "tanana")
ALGORITHM = "HS256"



class PayloadDTO(BaseModel):
    restaurant_user_id: int
    merchant_id: int
    email: str
    name: str
    exp: int
    

class EmailPayloadDTO(BaseModel):
    merchant_id: int
    permissions: MerchantUserRole
    email: str
    exp: int

def create_access_token(user: MerchantUser, expires_delta: Optional[timedelta] = None):
    payload: Dict[str, str|int] = {
        "restaurant_user_id": user.id,
        "merchant_id": user.merchant_id,
        "email": user.email,
        "name": user.name
    }
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=3)
    payload["exp"] =  expire
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_new_user_email_token(admin: MerchantUser, user: MerchantUserCreateTokenDTO ,expires_delta: Optional[timedelta] = None):
    payload: Dict[str, Any] = {
        "merchant_id": admin.merchant_id,
        "permissions": user.permissions.value,
        "email": user.email
        
    }
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=12)
    payload["exp"] =  expire
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_email_token(token: str):
    try:
        payload_dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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
        payload_dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        payload = PayloadDTO(**payload_dict)
        return payload
    except JWTError:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )




