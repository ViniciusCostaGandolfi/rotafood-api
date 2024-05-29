from typing import List, Optional
from api.config.custom_model import CustomModel
from api.domain.catalog.dtos.option_dto import OptionDto
from api.domain.catalog.models.status import Status

class OptionGroupDto(CustomModel):
    id: Optional[str] = None
    name: str
    status: Status
    optionGroupType: str
    options: List[OptionDto]