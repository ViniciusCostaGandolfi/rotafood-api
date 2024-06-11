from decimal import Decimal
from typing import Optional
from api.config.custom_model import CustomModel

class ScalePriceDto(CustomModel):
    id: Optional[str] = None
    minQuantity: str
    value: Decimal