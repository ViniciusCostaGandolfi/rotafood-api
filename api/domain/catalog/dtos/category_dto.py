from typing import List, Optional
from api.config.custom_model import CustomModel
from api.domain.catalog.dtos.item_dto import ItemDto
from api.domain.catalog.models.category_template import CategoryTemplate
from api.domain.catalog.models.status import Status


class CategoryDto(CustomModel):
    id: Optional[str] = None
    name: str
    index: int
    status: Status
    template: CategoryTemplate
    items: List[ItemDto]
    
class CategoryUpdateDto(CustomModel):
    name: str
    index: int
    status: Status
    template: CategoryTemplate
