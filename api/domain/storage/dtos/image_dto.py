from typing import Optional
from api.config.custom_model import CustomModel
from api.domain.storage.models.image_origin import ImageOrigin

class ImageDto(CustomModel):
    id: Optional[str] = None
    image_path: str
    image_origin: ImageOrigin
