from fastapi import APIRouter
from orders.controllers.order_controller import order_router


orders_router = APIRouter()
orders_router.include_router(order_router)