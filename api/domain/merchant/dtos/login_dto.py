

from pydantic import EmailStr
from api.config.pydantic import CustonModel


class LoginDto(CustonModel):
    email: EmailStr
    password: str