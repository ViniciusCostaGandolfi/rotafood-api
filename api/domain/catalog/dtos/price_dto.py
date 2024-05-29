from decimal import Decimal
from typing import List, Optional
from api.config.custom_model import CustomModel
from api.domain.catalog.models.scale_price import ScalePrice

class PriceDto(CustomModel):
    id: Optional[str] = None
    value: Decimal
    original_value: Decimal
    scale_prices: List[ScalePrice]