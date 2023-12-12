from fastapi import APIRouter, FastAPI
from restaurants.controllers.restaurant_controller import restaurant_router
from restaurants.controllers.restaurant_user_controller import restaurant_user_router


app = FastAPI()

app.include_router(restaurant_router, prefix='/accounts')
app.include_router(restaurant_user_router, prefix='/accounts')
