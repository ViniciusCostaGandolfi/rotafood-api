from fastapi import APIRouter
from controllers.catalog_controller import catalog_router


catalogs_router = APIRouter()

catalogs_router.include_router(catalog_router)