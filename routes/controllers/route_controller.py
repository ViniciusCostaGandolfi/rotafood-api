from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
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




route_router = APIRouter(prefix='/routes')

class RouteController:
    
    @route_router.get("/", response_model=List[RouteDTO])
    async def get_orders(
            current_user: MerchantUser = Depends(get_current_user),
            db: Session = Depends(get_db)
            ):
        
        
        routes = db.query(Route).filter(Route.merchant_id == current_user.merchant_id).order_by(desc(Route.id)).all()
        routes = [RouteDTO.model_validate(route) for route in routes]
        return routes
    
    @route_router.get("/{route_id}", response_model=OrderDTO)
    async def get_route_by_id(
            route_id:int,
            current_user: MerchantUser = Depends(get_current_admin_user),
            db: Session = Depends(get_db)):
        
        route = db.query(Route).filter(Route.id == route_id, Route.merchant_id == current_user.merchant_id).first()
        if not route:
            raise HTTPException(status_code=404, detail="No route with this ID or Not Authorized")
        
        return RouteDTO.model_validate(route)

    
    @route_router.post("/", response_model=List[RouteDTO])
    async def make_routes(
            current_user: MerchantUser = Depends(get_current_admin_user),
            db: Session = Depends(get_db)) -> OrderDTO:
        orders = db.query(Order).join(OrderDelivery).filter(
            Order.merchant_id == current_user.merchant_id, 
            OrderDelivery.delivered_by == "MERCHANT").all()
        
        print("O len de orders é", len(orders))
        if len(orders) < 2:
            HTTPException(401, "No Orders to Routine")
    
        
        origin = db.query(Merchant).filter(Merchant.id == current_user.merchant_id).first()
        
        origin = MerchantDTO.model_validate(origin)
        orders = [OrderDTO.model_validate(order) for order in orders]
        orders = [CVRPOrder(id=order.id, total_volume=order.total_volume, address=order.delivery.address) for order in orders]
        cvrp_in = CVRPIn(orders=orders, origin=origin, drivers_volume=45)
        url = os.getenv('ROTAFOOD_MS_ROUTES_URL') + '/CVR/'

        with httpx.Client() as client:
            cvrp_out = client.post(url, content=cvrp_in.model_dump_json(), timeout=600)
            
        if cvrp_out.status_code != 201:
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
 
        
        routes = [RouteDTO.model_validate(route) for route in routes]  
        
        return routes