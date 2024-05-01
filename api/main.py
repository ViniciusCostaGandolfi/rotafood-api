from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.controller.auth_controller import auth_controller
from api.controller.logistic_controller import logistic_controller




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



app.include_router(auth_controller)
app.include_router(logistic_controller)