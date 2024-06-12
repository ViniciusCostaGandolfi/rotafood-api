from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from api.controller.v1.auth_controller import auth_controller
from api.controller.v1.merchant_controller import merchant_controller
from api.controller.v1.logistic_controller import logistic_controller
from api.controller.v1.catalog_controller import catalog_controller
from api.controller.v1.category_controller import category_controller
from api.controller.v1.product_controller import product_controller
from api.controller.v1.item_controller import item_controller


v1_router = APIRouter()

v1_router.include_router(auth_controller)
v1_router.include_router(logistic_controller)
v1_router.include_router(merchant_controller)
v1_router.include_router(catalog_controller)
v1_router.include_router(category_controller)
v1_router.include_router(product_controller)
v1_router.include_router(item_controller)