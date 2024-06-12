from typing import TYPE_CHECKING, List, Optional
from api.config.custom_model import CustomModel
from api.domain.catalog.models.category_template import CategoryTemplate
from api.domain.catalog.models.status import Status

if TYPE_CHECKING:
    from api.domain.catalog.dtos.item_dto import FullItemDto


class FullCategoryDto(CustomModel):
    id: Optional[str] = None
    name: str
    index: int
    status: Status
    template: CategoryTemplate
    items: List['FullItemDto']
    
class CategoryDto(CustomModel):
    id: Optional[str] = None
    name: str
    index: int
    status: Status
    
class CategoryUpdateDto(CustomModel):
    name: str
    index: int
    status: Status
    template: CategoryTemplate
