from pydantic import BaseModel



class IFoodOrderDto(BaseModel):
    id: int
    ifood_order_id: str