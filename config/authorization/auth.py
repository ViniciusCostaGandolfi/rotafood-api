import email
from typing import Callable
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from config.authorization.tokens import verify_token

from config.database import get_db
from merchants.models.merchant_user import MerchantUser, ModulePermissions

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_token(token)
    user = db.query(MerchantUser).filter(MerchantUser.email == payload.email).first()
    if user is None:
        raise credentials_exception
    return user

def has_permission(user: MerchantUser, permission: ModulePermissions) -> bool:
    return permission.value in user.permissions

def permission_dependency(permission: ModulePermissions) -> Callable:
    async def verify_permission(
        current_user: MerchantUser = Depends(get_current_user)
    ) -> MerchantUser:
        if not has_permission(current_user, permission):
            print(current_user.permissions, permission)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso Negado"
            )
        return current_user
    return verify_permission


async def verify_token_only(token:str = Depends(oauth2_scheme)):
    return verify_token(token)