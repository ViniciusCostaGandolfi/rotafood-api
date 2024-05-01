from api.config.pydantic import CustonModel


class TokenDto(CustonModel):
    token: str