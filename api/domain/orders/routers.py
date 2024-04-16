from fastapi import APIRouter
from controller.order_controller import order_controller


orders_router = APIRouter()
orders_router.include_router(order_controller)