from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from addresses.DTOs.address_dto import AddressDTO
from config.authorization.auth import get_current_admin_user, get_current_user
from config.database import get_db
from merchants.DTOs.merchant_dto import MerchantDTO
from merchants.models import merchant
from merchants.models.merchant import Merchant
from merchants.models.merchant_user import MerchantUser
from orders.DTOs.order_dto import OrderDTO
from orders.models.order import Order, OrderType
from orders.models.order_delivery import OrderDelivery
from routes.DTOs.route_dto import CVRPIn, CVRPOrder, CVRPOut, RouteDTO
from routes.models.route import Route
from sqlalchemy import desc, func, select
import os
import httpx

from routes.models.route_order import RouteOrder




routes_test_controller = APIRouter(prefix='/routes/test')


class RouteController:
    
    @routes_test_controller.post("/", response_model=CVRPOut)
    async def test_routes(
        cvrp_in: CVRPIn
    ):
        url = os.getenv('ROTAFOOD_MS_ROUTES_URL') + '/CVRP/'

        async with httpx.AsyncClient() as client:
            cvrp_out = await client.post(url, content=cvrp_in.model_dump_json(), timeout=600)
            
        if cvrp_out.status_code not in [200, 201]:
            HTTPException(401, "Error to request a ms-routes")
          
        cvrp_out = CVRPOut(**cvrp_out.json())
        
        return cvrp_out
    
    @routes_test_controller.post("/auto_generate/{number_of_points}/", response_model=CVRPOut)
    async def test_routes_autogenerate(
        number_of_points: int
    ):
        
        url = os.getenv('TEST_ROTAFOOD_MS_ROUTES_URL') + f'/CVRP/test/auto_generate/{number_of_points}/'
        async with httpx.AsyncClient() as client:
            cvrp_out = await client.post(url, timeout=600)
            
        if cvrp_out.status_code not in [200, 201]:
            HTTPException(401, "Error to request a ms-routes")
          
        print(f'\n\n\n{cvrp_out.json()}')
        cvrp_out = CVRPOut(**cvrp_out.json())
        
        return cvrp_out