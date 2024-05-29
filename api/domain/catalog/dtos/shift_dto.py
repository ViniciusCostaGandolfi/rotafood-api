
from datetime import datetime
from typing import List, Optional
from api.config.custom_model import CustomModel

class ShiftDto(CustomModel):
    id: Optional[str] = None
    start_time: datetime
    end_time: datetime
    monday: bool
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool
    saturday: bool
    sunday: bool