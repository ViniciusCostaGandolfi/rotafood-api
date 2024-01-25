from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from addresses.models.address import Address
from config.authorization.auth import get_current_user
from config.database import get_db
from merchants.models.merchant_user import MerchantUser
from orders.dtos.order_dto import OrderDto
from orders.models.order import Order, OrderType
from orders.models.order_consumers import OrderCustomer
from orders.models.order_delivery import OrderDelivery
from orders.models.order_items import OrderItem
from orders.models.order_payments import OrderPayment


order_controller = APIRouter(prefix='/orders', tags=['Order'])


class ProductController:
    
    @order_controller.get("/", response_model=List[OrderDto])
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
        
        orders = [OrderDto.model_validate(order) for order in orders]
        return orders
    
    @order_controller.get("/{order_id}", response_model=OrderDto)
    async def get_order_by_id(
            order_id:int,
            db: Session = Depends(get_db)):
        
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="No order with this ID")
        
        return OrderDto.model_validate(order)

    
    @order_controller.put("/{order_id}", response_model=OrderDto)
    async def update_product(
            order_id:int,
            order_dto:OrderDto,
            current_user: MerchantUser = Depends(get_current_user),
            db: Session = Depends(get_db)) -> OrderDto:
        
        order =  db.query(Order).filter(Order.id == order_id, Order.merchant_id == current_user.merchant_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Product not found")
        
        
        for key, value in order_dto.model_dump().items():
            setattr(order, current_user, key, value)
      
        db.commit()
        
        return OrderDto.model_validate(order)
    
    @order_controller.post("/", response_model=OrderDto)
    def create_order(
            order_dto:OrderDto,
            user: MerchantUser = Depends(get_current_user),
            db: Session = Depends(get_db)) -> OrderDto:
        
    

        order = Order(order_type=order_dto.order_type,
                      order_timing=order_dto.order_timing,
                      created_at=order_dto.created_at,
                      preparation_start_datetime=order_dto.preparation_start_datetime,
                      total_volume=order_dto.total_volume,
                      total_price=order_dto.total_price,
                      merchant_id=user.merchant_id)
        
        
        db.add(order)
        db.commit()
        db.refresh(order)
        
        print(order_dto.items[0].model_dump())
 
        items = [OrderItem(
            quantity=item.quantity, 
            total_price=item.total_price, 
            total_volume=item.total_volume, 
            product_id=item.product.id,
            order_id=order.id) for item in order_dto.items]
        
        
        db.add_all(items)
        db.commit()
        for item in items:
            db.refresh(item)
        
        
        # if order_dto.payment is not None:
        #     print('payment')
        #     payment = OrderPayment(**order_dto.payment.model_dump(), order_id=order.id)
        #     db.add(payment)
        #     db.commit()
        #     db.refresh(payment)
        if order_dto.delivery is not None:
            address = Address(**order_dto.delivery.address.model_dump())
            db.add(address)
            db.commit()
            db.refresh(address)
            print(f"Address ID: {address.id}")
            
            delivery = OrderDelivery(
                **order_dto.delivery.model_dump(exclude={"address"}), 
                address_id=address.id, 
                order_id=order.id)
            db.add(delivery)
            db.commit()
            db.refresh(delivery)
            
            print(f"OrderDelivery ID: {delivery.id}")

        # if order_dto.order_customer is not None:
        #     print('customer')
        #     customer = OrderCustomer(**order_dto.order_customer.model_dump(), order_id=order.id)
        #     db.add(customer)
        #     db.commit()
        #     db.refresh(customer)
            
        return OrderDto.model_validate(order)