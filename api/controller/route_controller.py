from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
import os
import httpx
from typing import List

from api.core.authorization.auth import permission_dependency, get_current_user
from api.core.database import get_db
from api.domain.merchants.dtos.merchant_dto import MerchantDto
from api.domain.merchants.models.merchant import Merchant
from api.domain.merchants.models.merchant_user import MerchantUser, ModulePermissions
from api.domain.orders.dtos.order_dto import OrderDto
from api.domain.orders.models.order import Order
from api.domain.routes.dtos.route_dto import CVRPIn, CVRPOrder, CVRPOut, RouteDto
from api.domain.orders.models.order_delivery import OrderDelivery
from api.domain.routes.models.route import Route
from api.domain.routes.models.route_order import RouteOrder





routes_controller = APIRouter(prefix='/routes', tags=['Routes'])
    
@routes_controller.get("/", response_model=List[RouteDto])
async def get_routes(
        current_user: MerchantUser = Depends(get_current_user),
        db: Session = Depends(get_db)
        ):
    
    
    routes = db.query(Route).filter(Route.merchant_id == current_user.merchant_id).order_by(desc(Route.id)).all()
    routes = [RouteDto.model_validate(route) for route in routes]
    return routes

@routes_controller.get("/{route_id}", response_model=OrderDto)
async def get_route_by_id(
        route_id:int,
        current_user: MerchantUser = Depends(
            permission_dependency(ModulePermissions.ROUTES)
            ),
        db: Session = Depends(get_db)):
    
    route = db.query(Route).filter(Route.id == route_id, Route.merchant_id == current_user.merchant_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="No route with this ID or Not Authorized")
    
    return RouteDto.model_validate(route)


@routes_controller.post("/", response_model=List[RouteDto])
async def make_routes(
        current_user: MerchantUser = Depends(
            permission_dependency(ModulePermissions.ROUTES)
            ),
        db: Session = Depends(get_db)):
    orders = db.query(Order).join(OrderDelivery).filter(
        Order.merchant_id == current_user.merchant_id, 
        OrderDelivery.delivered_by == "MERCHANT").all()
    
    if len(orders) < 2:
        HTTPException(401, "No Orders to Routine")

    
    merchant_db = db.query(Merchant).filter(Merchant.id == current_user.merchant_id).first()
    
    merchant = MerchantDto.model_validate(merchant_db)
    orders = [OrderDto.model_validate(order) for order in orders]
    orders = [CVRPOrder(id=order.id, total_volume=order.total_volume, address=order.delivery.address) for order in orders]
    cvrp_in = CVRPIn(orders=orders, merchant=merchant, drivers_volume=45)
    url = os.getenv('TEST_ROTAFOOD_MS_ROUTES_URL') if os.getenv('ENVMODE') == 'DEVELOP' else os.getenv('ROTAFOOD_MS_ROUTES_URL')

    url += '/CVRP/'

    with httpx.Client() as client:
        cvrp_out = client.post(url, content=cvrp_in.model_dump_json(), timeout=600)
        
    if cvrp_out.status_code not in [200, 201]:
        HTTPException(401, "Error to request a ms-routes")
        
    cvrp_out = CVRPOut(**cvrp_out.json())
    routes = []
    for route in cvrp_out.routes:
        route_db = Route(**route.model_dump(exclude="orders"), merchant_id=current_user.merchant_id)
        db.add(route_db)
        db.commit()
        db.refresh(route_db)
        routes.append(route_db)
        
        for i in range(len(route.orders)):
            route_order = route.orders[i]
            route_order = RouteOrder(order_id=route_order.id, route_id=route_db.id, index=route.sequence[i])
            db.add(route_order)
            db.commit() 
            db.refresh(route_order)

    
    routes = [RouteDto.model_validate(route) for route in routes]  
    
    return routes

