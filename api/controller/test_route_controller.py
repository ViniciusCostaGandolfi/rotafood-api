from fastapi import APIRouter, HTTPException

from api.domain.merchants.dtos.merchant_dto import MerchantDto

from  api.domain.routes.dtos.route_dto import CVRPIn, CVRPOut, CVRPRoute
import os
import httpx
from api.core.helpers import url





routes_test_controller = APIRouter(prefix='/routes/test', tags=['TestRoutes'])



@routes_test_controller.post("/", response_model=CVRPOut)
async def test_routes(
    cvrp_in: CVRPIn
):
    url_api = url + '/CVRP/'

    async with httpx.AsyncClient() as client:
        cvrp_out = await client.post(url_api, content=cvrp_in.model_dump_json(), timeout=600)
        
    if cvrp_out.status_code not in [200, 201]:
        HTTPException(401, "Error to request a ms-routes")
        
    cvrp_out = CVRPOut(**cvrp_out.json())
    
    return cvrp_out



 
  
@routes_test_controller.post("/auto_generate/{number_of_orders}/", response_model=CVRPOut)
async def test_routes_autogenerate(      
    number_of_orders: int, 
    merchant: MerchantDto      
):                                          
      
    if number_of_orders > 500:
        return HTTPException(401, "O máximo de pontos por pesquisa é 500")
    url_api = url + f'/CVRP/test/auto_generate/{number_of_orders}/'
    async with httpx.AsyncClient() as client:
        cvrp_out = await client.post(url_api, content=merchant.model_dump_json(), timeout=600)
         
            
           
    if cvrp_out.status_code != 200:
        HTTPException(401, "Error to request a ms-routes")
        
    cvrp_out = CVRPOut(**cvrp_out.json())
    cvrp_out.routes = [CVRPRoute(
        id=i,
        **route.model_dump(exclude=['id'])
        
        ) for i, route in enumerate(cvrp_out.routes)]
    
    return cvrp_out 