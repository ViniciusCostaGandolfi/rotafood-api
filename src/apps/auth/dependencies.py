import email
from typing import Callable
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth.services.token_service import verify_token
from merchants.dtos.merchant_user_dto import MerchantUserDto
from merchants.models.merchant_user import ModulePermissions
from exceptions import not_allowed_exception

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)

def has_permission(user: MerchantUserDto, permission: ModulePermissions) -> bool:
    return permission.value in user.permissions

def permission_dependency(permission: ModulePermissions) -> Callable:
    async def verify_permission(
        current_user: MerchantUserDto = Depends(get_current_user)
    ) -> MerchantUserDto:
        if not has_permission(current_user, permission):   
            return not_allowed_exception     
        return current_user
    return verify_permission