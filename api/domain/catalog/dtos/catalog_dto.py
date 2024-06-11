from datetime import datetime
from typing import List, Optional
from api.config.custom_model import CustomModel
from api.domain.catalog.dtos.category_dto import CategoryDto
from api.domain.catalog.models.catalog_context_modifier import CatalogContextModifier
    
    
class CatalogDto(CustomModel):
    id: Optional[str] = None
    name: str
    modified_at: datetime
    catalog_context_modifier: CatalogContextModifier
    categories: List[CategoryDto]
    
class CatalogUpdateDto(CustomModel):
    id: Optional[str] = None
    name: str
    catalog_context_modifier: str