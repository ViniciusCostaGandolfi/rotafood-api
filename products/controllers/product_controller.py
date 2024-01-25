from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.authorization.auth import get_current_user
from config.database import get_db
from merchants.models.merchant_user import MerchantUser
from products.dtos.product_dto import ProductDto
from products.models.product import Product
from products.models.product_category import ProductCategory


product_controller = APIRouter(prefix='/products', tags=['Product'])

class ProductController:
    
    @product_controller.get("/", response_model=List[ProductDto])
    async def get_products(
            current_user: MerchantUser = Depends(get_current_user),
            db: Session = Depends(get_db)
            ):
        products =  db.query(Product).filter(Product.merchant_id == current_user.merchant_id).all()
        if not products:
            raise HTTPException(status_code=401, detail="No products")
        return ProductDto.model_validate(products)
    
    @product_controller.get("/{product_id}", response_model=ProductDto)
    async def get_product_by_id(
            product_id:int,
            db: Session = Depends(get_db)):
        
        product =  db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="No product with this")
        return ProductDto.model_validate(product)

    
    @product_controller.put("/{product_id}", response_model=ProductDto)
    async def update_product(
            product_id:int,
            product_dto:ProductDto,
            current_user: MerchantUser = Depends(get_current_user),
            db: Session = Depends(get_db)) -> ProductDto:
        
        product =  db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        
        for key, value in product_dto.model_dump().items():
            setattr(product, current_user, key, value)
      
        db.commit()
        
        return ProductDto.model_validate(product)
    
    @product_controller.post("/", response_model=ProductDto)
    async def create_product(
            product_dto:ProductDto,
            current_user: MerchantUser = Depends(get_current_user),
            db: Session = Depends(get_db)) -> ProductDto:
        
        
        category: ProductCategory = db.query(ProductCategory).filter(ProductCategory.id == product_dto.category.id).first()
        if not category:
            raise HTTPException(status_code=401, detail="Category ID not exist")
        product =  Product(
            **product_dto.model_dump(exclude=['category', 'option_groups']), 
            merchant_id=current_user.merchant_id, category_id=category.id
            )
        
        print(f"\n\n  {product} \n\n")
        db.add(product)
        db.commit()
        db.refresh(product)
        
        
        return ProductDto.model_validate(product)
    