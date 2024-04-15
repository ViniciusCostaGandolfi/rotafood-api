from fastapi import APIRouter
from routes.controllers.route_controller import routes_controller
from routes.controllers.test_route_controller import routes_test_controller


routes_router = APIRouter()
 
routes_router.include_router(routes_controller)
routes_router.include_router(routes_test_controller)