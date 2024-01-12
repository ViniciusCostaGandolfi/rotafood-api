from fastapi import APIRouter, FastAPI
from merchants.routers import merchants_routers
from products.routers import products_router
from catalog.routers import catalogs_router
from orders.routers import orders_router
from routes.routers import routes_router


app = FastAPI()

app.include_router(merchants_routers)
app.include_router(products_router)
app.include_router(catalogs_router)
app.include_router(orders_router)
app.include_router(routes_router)