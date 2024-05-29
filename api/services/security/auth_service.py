import email
from typing import Callable
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from api.services.database_service import get_db
from api.services.security.decode_token_service import verify_token
from api.domain.merchant.dtos.merchant_user_dto import MerchantUserDto
from api.domain.merchant.models.merchant_permission import MerchantPermission

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)

def has_permission(user: MerchantUserDto, permission: MerchantPermission) -> bool:
    return permission.value in user.permissions

def permission_dependency(permission: MerchantPermission) -> Callable:
    async def verify_permission(
        current_user: MerchantUserDto = Depends(get_current_user)
    ) -> MerchantUserDto:
        if not has_permission(current_user, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso Negado"
            )
        return current_user
    return verify_permission