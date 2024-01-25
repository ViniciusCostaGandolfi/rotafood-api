from fastapi import APIRouter, HTTPException

from merchants.dtos.merchant_dto import MerchantDto

from routes.dtos.route_dto import CVRPIn, CVRPOut
import os
import httpx





routes_test_controller = APIRouter(prefix='/routes/test', tags=['TestRoutes'])



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





@routes_test_controller.post("/auto_generate/{number_of_orders}/", response_model=CVRPOut)
async def test_routes_autogenerate(
    number_of_orders: int,
    merchant: MerchantDto
):
    
    url = os.getenv('TEST_ROTAFOOD_MS_ROUTES_URL') + f'/CVRP/test/auto_generate/{number_of_orders}/'
    print(url)
    async with httpx.AsyncClient() as client:
        cvrp_out = await client.post(url, content=merchant.model_dump_json(), timeout=600)
        
    if cvrp_out.status_code not in [200, 201]:
        HTTPException(401, "Error to request a ms-routes")
        
    print(f'\n\n\n{cvrp_out.json()}')
    cvrp_out = CVRPOut(**cvrp_out.json())
    
    return cvrp_out 