from fastapi import APIRouter
from routes.controllers.route_controller import route_router


routes_router = APIRouter()

routes_router.include_router(route_router)