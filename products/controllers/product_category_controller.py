from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.authorization.auth import get_current_user
from config.database import get_db
from merchants.models.merchant_user import MerchantUser
from products.dtos.product_dto import CategoryDto
from products.models.product_category import ProductCategory


category_controller = APIRouter(prefix='/product_category', tags=['ProductCategory'])

@category_controller.get("/", response_model=List[CategoryDto])
async def get_product_categories(
        current_user: MerchantUser = Depends(get_current_user),
        db: Session = Depends(get_db)
        ):
    categories_db =  db.query(ProductCategory).filter(ProductCategory.merchant_id == current_user.merchant_id).all()
    
        
    return [CategoryDto.model_validate(category) for category in categories_db]

@category_controller.get("/{product_category_id}", response_model=CategoryDto)
async def get_product_category_by_id(
        product_category_id:int,
        db: Session = Depends(get_db)):
    
    product =  db.query(ProductCategory).filter(ProductCategory.id == product_category_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="No product with this")
    return CategoryDto.model_validate(product)


@category_controller.patch("/{product_category_id}", response_model=CategoryDto)
async def update_product_category(
        product_category_id:int,
        category_dto:CategoryDto,
        current_user: MerchantUser = Depends(get_current_user),
        db: Session = Depends(get_db)) -> CategoryDto:
    
    category =  db.query(ProductCategory).filter(ProductCategory.id == product_category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Product not found")
    
    
    for key, value in category_dto.model_dump().items():
        if value is not None:
            setattr(category, current_user, key, value)
    
    db.commit()
    db.refresh(category)
    
    return CategoryDto.model_validate(category)

@category_controller.post("/", response_model=CategoryDto)
async def create_product_category(
        category_dto:CategoryDto,
        current_user: MerchantUser = Depends(get_current_user),
        db: Session = Depends(get_db)) -> CategoryDto:
    
    
    category = ProductCategory(**category_dto.model_dump(), merchant_id=current_user.merchant_id)
    db.add(category)
    db.commit()
    db.refresh(category)
    
    
    return CategoryDto.model_validate(category)
