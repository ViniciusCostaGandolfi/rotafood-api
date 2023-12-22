from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.authorization.auth import get_current_user
from config.database import get_db
from merchants.models import merchant
from merchants.models.merchant_user import MerchantUser
from products.dtos.product_dto import ProductDTO
from products.models.product import Product
from products.models.product_category import ProductCategory


product_router = APIRouter(prefix='/products')

class ProductController:

    
    @product_router.get("/", response_model=List[ProductDTO])
    async def get_products(
            merchant_user_id:int,
            current_user: MerchantUser = Depends(get_current_user)
            ):
        return ProductDTO.model_validate(current_user)
    
    @product_router.get("/{product_id}", response_model=ProductDTO)
    async def get_product_by_id(
            product_id:int,
            db: Session = Depends(get_db)):
        
        product =  db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="User not found")
        return ProductDTO.model_validate(product)

    
    @product_router.put("/{product_id}", response_model=ProductDTO)
    async def update_merchant_user(
            product_id:int,
            product_dto:ProductDTO,
            current_user: MerchantUser = Depends(get_current_user),
            db: Session = Depends(get_db)) -> ProductDTO:
        
        product =  db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        
        for key, value in product_dto.model_dump().items():
            setattr(product, current_user, key, value)
      
        db.commit()
        
        return ProductDTO.model_validate(product)
    
    @product_router.post("/", response_model=ProductDTO)
    async def update_merchant_user(
            product_dto:ProductDTO,
            current_user: MerchantUser = Depends(get_current_user),
            db: Session = Depends(get_db)) -> ProductDTO:
        
        category = ProductCategory(product_dto.category.model_dump())
        product =  Product(
            **product_dto.model_dump(exclude=['category', 'option_groups']), 
            merchant_id=current_user.merchant_id, category=category
            )
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
      
        db.commit()
        
        return ProductDTO.model_validate(product)
    