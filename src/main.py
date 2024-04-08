from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.merchants.routers import merchants_routers
from apps.products.routers import products_router
from apps.catalog.routers import catalogs_router
from apps.orders.routers import orders_router
from apps.routes.routers import routes_router



app = FastAPI(
    
    title='RotaFood API',
    description='''
    O RotaFood API é a api do meu site project RotaFood!
    Um sistema de roterização para restaurantes com um 
    ERP acoplado.
    ''',
    version='v1'
)

# Vou tentar vender uma API
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(merchants_routers)
app.include_router(products_router)
app.include_router(catalogs_router)
app.include_router(orders_router)
app.include_router(routes_router)