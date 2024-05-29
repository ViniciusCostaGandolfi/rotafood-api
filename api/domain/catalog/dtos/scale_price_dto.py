from decimal import Decimal
from typing import Optional
from api.config.custom_model import CustomModel

class PriceDto(CustomModel):
    id: Optional[str] = None
    minQuantity: str
    value: Decimal