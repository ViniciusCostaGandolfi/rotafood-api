from typing import Optional
from api.config.custom_model import CustomModel
from api.domain.catalog.dtos.product_dto import ProductDto
from api.domain.catalog.models.status import Status

class OptionDto(CustomModel):
    id: Optional[str] = None
    name: str
    status: Status
    index: int
    product: ProductDto