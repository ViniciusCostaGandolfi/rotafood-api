from enum import Enum
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from config.authorization.auth import get_current_admin_user, get_current_user
from config.database import get_db
from merchants.models import merchant
from merchants.models.merchant_user import MerchantUser
from orders.DTOs.order_dto import OrderDTO
from orders.models.order import Order, OrderType
from orders.models.order_consumers import OrderCustomer
from orders.models.order_delivery import OrderDelivery
from orders.models.order_items import OrderItem
from orders.models.order_payments import OrderPayment



order_router = APIRouter(prefix='/orders')


class ProductController:
    
    @order_router.get("/", response_model=List[OrderDTO])
    async def get_orders(
            order_type: Optional[OrderType] = None,
            current_user: MerchantUser = Depends(get_current_user),
            db: Session = Depends(get_db)
            ):
        
        if order_type is None:
            orders = db.query(Order).filter(Order.merchant_id == current_user.merchant_id) 
            
        if order_type is not None:
            orders = db.query(Order).filter(Order.merchant_id == current_user.merchant_id, order_type == order_type.value)
    
        if orders is None:
            raise HTTPException(status_code=401, detail="No orders")
        
        orders = [OrderDTO.model_validate(order) for order in orders]
        return orders
    
    @order_router.get("/{order_id}", response_model=OrderDTO)
    async def get_order_by_id(
            order_id:int,
            db: Session = Depends(get_db)):
        
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="No order with this ID")
        
        return OrderDTO.model_validate(order)

    
    @order_router.put("/{order_id}", response_model=OrderDTO)
    async def update_product(
            order_id:int,
            order_dto:OrderDTO,
            current_user: MerchantUser = Depends(get_current_user),
            db: Session = Depends(get_db)) -> OrderDTO:
        
        order =  db.query(Order).filter(Order.id == order_id, Order.merchant_id == current_user.merchant_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Product not found")
        
        
        for key, value in order_dto.model_dump().items():
            setattr(order, current_user, key, value)
      
        db.commit()
        
        return OrderDTO.model_validate(order)
    
    @order_router.post("/", response_model=OrderDTO)
    async def create_product(
            order_dto:OrderDTO,
            user: MerchantUser = Depends(get_current_user),
            db: Session = Depends(get_db)) -> OrderDTO:
        
        order = Order(**order_dto.model_dump(exclude=['items', 'payment', 'customer', 'delivery']), merchant_id=user.merchant_id)
        db.add(order)
        
        items = [OrderItem(**item, order_id=order.id) for item in order_dto.items]
        db.add_all(items)
        
        if order_dto.payment:
            payment = OrderPayment(order_dto.payment, order_id=order.id)
            db.add(payment)
        if order_dto.delivery:
            delivery = OrderDelivery(order_dto.delivery, order_id=order.id)
            db.add(delivery)
        if order_dto.customer:
            customer = OrderCustomer(order_dto.customer, order_id=order.id)
            db.add(customer)
        db.commit()
        return OrderDTO.model_validate(order)