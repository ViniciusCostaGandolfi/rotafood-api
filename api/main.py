from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from api.controller.v1.auth_controller import auth_controller
from api.controller.v1.merchant_controller import merchant_controller
from api.controller.v1.logistic_controller import logistic_controller




app = FastAPI(
    
    title='RotaFood API',
    description='''
    O RotaFood API é a api do meu site project RotaFood!
    Um sistema de roterização para restaurantes com um 
    ERP acoplado.
    ''',
    version='v1',
)

# Vou tentar vender uma API
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse('favicon.ico')

app.include_router(auth_controller)
app.include_router(logistic_controller)
app.include_router(merchant_controller)