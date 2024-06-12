from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from api.controller.v1.router import v1_router


app = FastAPI(
    
    title='RotaFood API',
    description='''
    O RotaFood API é a api do meu site project RotaFood!
    ''',
    version='v1',
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"}
)

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

app.include_router(v1_router)