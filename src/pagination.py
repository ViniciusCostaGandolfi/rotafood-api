from typing import List, Optional
import os
from typing import Generic, TypeVar
from custom_model import CustomModel
    
T = TypeVar("T")

class Paginable(CustomModel, Generic[T]):
    current_page: int
    total_pages: int
    page_size: int
    total_count: int
    data: List[T]
    previous_page: Optional[int] = None
    next_page: Optional[int] = None

def paginate(items: List[T], page: int, page_size: int) -> Paginable[T]:
    total_count = len(items)
    total_pages = (total_count - 1) // page_size + 1
    
    previous_page = max(1, page - 1) if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    return Paginable(
        current_page=page,
        total_pages=total_pages,
        page_size=page_size,
        total_count=total_count,
        data=items,
        previous_page=previous_page,
        next_page=next_page
    )