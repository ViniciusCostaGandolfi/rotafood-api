from typing import List, Optional
from api.config.custom_model import CustomModel
from api.domain.catalog.dtos.item_dto import ItemDto


class CategoryDto(CustomModel):
    id: Optional[str] = None
    modified_at: str
    catalog_context_modifier: str
    items: List[ItemDto]