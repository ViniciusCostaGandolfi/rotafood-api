from typing import TYPE_CHECKING, List, Optional

from pydantic import UUID4
from api.config.custom_model import CustomModel
from api.domain.catalog.dtos.context_modifier_dto import ContextModifierDto
from api.domain.catalog.dtos.option_group_dto import OptionGroupDto
from api.domain.catalog.dtos.price_dto import PriceDto
from api.domain.catalog.dtos.product_dto import ProductDto
from api.domain.catalog.dtos.shift_dto import ShiftDto
from api.domain.catalog.models.status import Status
from api.domain.catalog.dtos.category_dto import CategoryDto

class FullItemDto(CustomModel):
    id: Optional[UUID4] = None
    type: str
    status: Status
    index: int
    product: ProductDto
    category: CategoryDto
    price: PriceDto
    shifts: List[ShiftDto]
    context_modifiers: List[ContextModifierDto]
    option_groups: Optional[List[OptionGroupDto]]
    
