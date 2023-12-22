from fastapi import APIRouter, FastAPI
from merchants.routers import merchants_routers


app = FastAPI()

app.include_router(merchants_routers)