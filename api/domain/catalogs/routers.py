from fastapi import APIRouter
from controller.catalog_controller import catalog_router


catalogs_router = APIRouter()

catalogs_router.include_router(catalog_router)