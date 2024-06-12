from typing import List, Optional
from api.config.custom_model import CustomModel
from api.domain.catalog.dtos.price_dto import PriceDto
from api.domain.catalog.dtos.product_dto import ProductDto
from api.domain.catalog.models.dietary_restrictions import DietaryRestriction
from api.domain.catalog.models.product_type import ProductType
from api.domain.catalog.models.status import Status
from api.domain.storage.dtos.image_dto import ImageDto

class OptionDto(CustomModel):
    id: Optional[str] = None
    status: Status
    index: int
    price: PriceDto
    external_code: str
    product: ProductDto