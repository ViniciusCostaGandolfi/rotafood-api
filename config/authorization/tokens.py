from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from fastapi import HTTPException, status
from jose import JWTError, jwt
from pydantic import BaseModel
from restaurants.DTOs.restaurant_user_dto import RestaurantUserCreateTokenDTO

from restaurants.models.restaurant_user import RestaurantUser, Role

SECRET_KEY = "sua_chave_secreta"
ALGORITHM = "HS256"



class PayloadDTO(BaseModel):
    restaurant_user_id: int
    restaurant_id: int
    email: str
    name: str
    exp: int
    

class EmailPayloadDTO(BaseModel):
    restaurant_id: int
    permissions: Role
    email: str
    exp: int

def create_access_token(user: RestaurantUser, expires_delta: Optional[timedelta] = None):
    payload: Dict[str, Any] = {
        "restaurant_user_id": user.id,
        "restaurant_id": user.restaurant_id,
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

def create_new_user_email_token(admin: RestaurantUser, user: RestaurantUserCreateTokenDTO ,expires_delta: Optional[timedelta] = None):
    payload: Dict[str, Any] = {
        "restaurant_id": admin.restaurant_id,
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

def verify_token(token: str, credentials_exception):
    try:
        payload_dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        payload = PayloadDTO(**payload_dict)
        return payload
    except JWTError:
        raise credentials_exception


