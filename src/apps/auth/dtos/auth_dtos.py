from typing import List
from apps.merchants.models.merchant_user import ModulePermissions
from custom_model import CustomModel


class PayloadDTO(CustomModel):
    restaurant_user_id: int
    merchant_id: int
    email: str
    name: str
    exp: int
    

class EmailPayloadDTO(CustomModel):
    merchant_id: int
    permissions: List[ModulePermissions]
    email: str
    exp: int