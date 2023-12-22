import email
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from config.authorization.tokens import verify_token

from config.database import get_db
from merchants.models.merchant_user import MerchantUser, MerchantUserRole

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

async def get_current_admin_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_token(token)
    user:MerchantUser | None = db.query(MerchantUser).filter(MerchantUser.email == payload.email).first()
    
    if user is not None and user.permissions in [MerchantUserRole.OWNER, MerchantUserRole.ADM]:
        return user
    else:
        raise credentials_exception


async def verify_token_only(token:str = Depends(oauth2_scheme)):
    return verify_token(token)