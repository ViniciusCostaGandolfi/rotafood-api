from products.controllers.product_controller import product_controller
from products.controllers.product_category_controller import category_controller
from fastapi import APIRouter

products_router = APIRouter()

products_router.include_router(product_controller)
products_router.include_router(category_controller)


