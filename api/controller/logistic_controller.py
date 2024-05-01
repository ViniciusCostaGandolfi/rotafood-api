from datetime import datetime, UTC
from fastapi import APIRouter, Depends, HTTPException
import httpx
from typing import List
import numpy as np 
from numpy.typing import NDArray
from numpy import float64
from sklearn.datasets import make_blobs

from api.config.config import ProductionSettings
from api.config.database import get_db
from api.domain.logistic.dtos.address_dto import AddressDto
from api.domain.logistic.dtos.cvrp_dto import CvrpBaseDto, CvrpInDto, CvrpOrderDto, CvrpOutDto
from api.domain.logistic.models import cvrp_in






logistic_controller = APIRouter(prefix='/routes', tags=['Routes'])

ms_logistic_url = ProductionSettings.ROTAFOOD_MS_LOGISTIC 
    
@logistic_controller.post("/", response_model=CvrpOutDto)
async def test_cvrp(
    cvrp_in: CvrpInDto
    ):
    url_api = ms_logistic_url + '/CVRP/'

    async with httpx.AsyncClient() as client:
        response = await client.post(url_api, content=cvrp_in.model_dump_json(), timeout=600)
        
    if response.status_code not in [200, 201]:
        HTTPException(401, "Error to request a ms-routes")
        
    
    return CvrpOutDto(**response.json())



 
  
@logistic_controller.post("/auto_generate/{number_of_orders}/", response_model=CvrpOutDto)
async def test_cvrp_autogenerate(      
    number_of_orders: int, 
    address: AddressDto      
    ):                                          
      
    if number_of_orders > 500:
        return HTTPException(401, "O máximo de pontos por pesquisa é 500")
    
    center = np.array([[address.latitude, address.longitude]]) 
    std = [0.003]
    localities, _ = make_blobs(n_samples=number_of_orders, centers=center, cluster_std=std) # type: ignore
    orders_volumes: List[float] = np.random.normal(7, 3, number_of_orders).tolist()
        
    cvrp_in = CvrpInDto(
        base=CvrpBaseDto(address=address),
        max_route_volume = 45,
        orders=[CvrpOrderDto(
            total_volume=orders_volumes[i],
            create_at=int(datetime.now(UTC).timestamp()),
            address=AddressDto(
                street_name='str',
                formatted_address='str',
                street_number='str',
                city='str',
                postal_code='str',
                neighborhood='str',
                state='str',
                complement='str',
                latitude=localities[i, 0],
                longitude=localities[i, 1]

            )
            ) for i in np.arange(number_of_orders)],
    )
    url_api = ms_logistic_url + f'/CVRP/'
    
    async with httpx.AsyncClient() as client:
        cvrp_out = await client.post(url_api, content=address.model_dump_json(), timeout=600)
         
    if cvrp_out.status_code != 200:
        HTTPException(401, "Error to request a ms-routes")
            
    return CvrpOutDto(**cvrp_out.json()) 

