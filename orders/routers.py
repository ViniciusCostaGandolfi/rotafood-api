from fastapi import APIRouter
from orders.controllers.order_controller import order_controller


orders_router = APIRouter()
orders_router.include_router(order_controller)