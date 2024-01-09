from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.authorization.auth import get_current_admin_user, get_current_user
from config.database import get_db
from merchants.models.merchant import Merchant
from merchants.models.merchant_user import MerchantUser
from orders.DTOs.order_dto import OrderDTO
from orders.models.order import Order
from routes.DTOs.route_dto import CVRPIn, CVRPOut, RouteDTO
from routes.models.route import Route
from sqlalchemy import desc, func, select
import os
import httpx




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

    
    @route_router.post("/", response_model=RouteDTO)
    async def create_product(
            current_user: MerchantUser = Depends(get_current_admin_user),
            db: Session = Depends(get_db)) -> OrderDTO:
        
        orders = db.query(Order).filter(Order.order_type == 'DELIVERY', Order.delivery.delivered_by == 'MERCHANT')
        if not orders:
            HTTPException(status_code=401, detail="No orders to make routes")
        if len(orders) > 1:
            pass
        
        origin = db.query(Merchant).filter(Merchant.id == current_user.merchant_id).first()
        cvrp_in = CVRPIn(orders=orders, origin=origin, drivers_volume=45)
        
        url = os.getenv('ROTAFOOD_MS_ROUTES_URL') + '/CVR'
        async with httpx.AsyncClient() as client:
            cvrp_out: CVRPOut = await client.post(url, json=cvrp_in.model_dump())
            
        for route in cvrp_out.routes:
            pass
        db.commit() 
            
        return RouteDTO.model_validate(route)
    # @route_router.put("/{order_id}", response_model=OrderDTO)
    # async def update_product(
    #         order_id:int,
    #         order_dto:OrderDTO,
    #         current_user: MerchantUser = Depends(get_current_user),
    #         db: Session = Depends(get_db)) -> OrderDTO:
        
    #     order =  db.query(Order).filter(Order.id == order_id, Order.merchant_id == current_user.merchant_id).first()
    #     if not order:
    #         raise HTTPException(status_code=404, detail="Product not found")
        
        
    #     for key, value in order_dto.model_dump().items():
    #         setattr(order, current_user, key, value)
      
    #     db.commit()
        
    #     return OrderDTO.model_validate(order)
    