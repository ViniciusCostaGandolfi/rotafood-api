from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.controller.authentication_controller import authenticaion_controller
from api.controller.merchant_user_controller import merchant_user_controller
from api.controller.merchant_controller import merchant_controller
from api.controller.product_controller import product_controller
from api.controller.category_controller import category_controller
from api.controller.order_controller import order_controller
from api.controller.catalog_controller import catalog_controller
from api.controller.route_controller import routes_controller
from api.controller.test_route_controller import routes_test_controller




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


app.include_router(merchant_controller)
app.include_router(merchant_user_controller)
app.include_router(authenticaion_controller)
app.include_router(product_controller)
app.include_router(category_controller)
app.include_router(catalog_controller)
app.include_router(order_controller)
app.include_router(routes_controller)
app.include_router(routes_test_controller)