from typing import List, Optional
from api.config.custom_model import CustomModel
from api.domain.catalog.dtos.option_group_dto import OptionGroupDto
from api.domain.catalog.models.dietary_restrictions import DietaryRestriction
from api.domain.catalog.models.product_type import ProductType
from api.domain.storage.dtos.image_dto import ImageDto

class ProductDto(CustomModel):
    id: Optional[str] = None
    name: str
    description: str
    ean: int
    additional_information: str
    type: ProductType
    dietary_restrictions: List[DietaryRestriction]
    option_groups: List[OptionGroupDto]
    image: ImageDto