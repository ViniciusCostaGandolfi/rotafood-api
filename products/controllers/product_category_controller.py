from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.authorization.auth import get_current_user
from config.database import get_db
from merchants.models import merchant
from merchants.models.merchant_user import MerchantUser
from products.dtos.product_dto import CategoryDTO
from products.models.product import Product
from products.models.product_category import ProductCategory


category_router = APIRouter(prefix='/category')

class CategoryController:
    @category_router.get("/", response_model=List[CategoryDTO])
    async def get_products(
            current_user: MerchantUser = Depends(get_current_user),
            db: Session = Depends(get_db)
            ):
        products =  db.query(ProductCategory).filter(ProductCategory.merchant_id == current_user.merchant_id).all()
        if not products:
            raise HTTPException(status_code=401, detail="No products")
        return CategoryDTO.model_validate(products)
    
    @category_router.get("/{product_category_id}", response_model=CategoryDTO)
    async def get_product_by_id(
            product_category_id:int,
            db: Session = Depends(get_db)):
        
        product =  db.query(ProductCategory).filter(ProductCategory.id == product_category_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="No product with this")
        return CategoryDTO.model_validate(product)

    
    @category_router.patch("/{product_category_id}", response_model=CategoryDTO)
    async def update_product(
            product_category_id:int,
            category_dto:CategoryDTO,
            current_user: MerchantUser = Depends(get_current_user),
            db: Session = Depends(get_db)) -> CategoryDTO:
        
        category =  db.query(ProductCategory).filter(ProductCategory.id == product_category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Product not found")
        
        
        for key, value in category_dto.model_dump().items():
            if value is not None:
                setattr(category, current_user, key, value)
      
        db.commit()
        
        return CategoryDTO.model_validate(category)
    
    @category_router.post("/", response_model=CategoryDTO)
    async def create_product(
            product_dto:CategoryDTO,
            current_user: MerchantUser = Depends(get_current_user),
            db: Session = Depends(get_db)) -> CategoryDTO:
        
        
        category = ProductCategory(**product_dto.model_dump(), merchant_id=current_user.merchant_id)
      
        db.commit()
        
        return CategoryDTO.model_validate(category)
    