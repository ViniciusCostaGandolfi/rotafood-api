from typing import List, Optional
from api.config.custom_model import CustomModel
from api.domain.catalog.dtos.context_modifier_dto import ContextModifierDto
from api.domain.catalog.dtos.price_dto import PriceDto
from api.domain.catalog.dtos.product_dto import ProductDto
from api.domain.catalog.dtos.shift_dto import ShiftDto
from api.domain.catalog.models.status import Status

class ItemDto(CustomModel):
    id: Optional[str] = None
    type: str
    status: Status
    index: int
    product: ProductDto
    price: PriceDto
    shifts: List[ShiftDto]
    context_modifier: List[ContextModifierDto]
    catedory_id: str
    merchant_id: str