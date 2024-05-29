from typing import Optional
from api.config.custom_model import CustomModel
from api.domain.catalog.dtos.price_dto import PriceDto
from api.domain.catalog.models.catalog_context_modifier import CatalogContextModifier

class ContextModifierDto(CustomModel):
    id: Optional[str] = None
    price: PriceDto
    catalog_context_modifier: CatalogContextModifier

