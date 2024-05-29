from pydantic import EmailStr
from api.config.custom_model import CustomModel


class LoginDto(CustomModel):
    email: EmailStr
    password: str