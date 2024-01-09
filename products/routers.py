from products.controllers.product_controller import product_router
from products.controllers.product_category_controller import category_router
from fastapi import APIRouter

products_router = APIRouter()

products_router.include_router(product_router)
products_router.include_router(category_router)


