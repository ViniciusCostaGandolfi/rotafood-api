from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
from config.authorization.auth import get_current_user
from config.database import get_db
from config.helpers import Paginable
from merchants.models.merchant_user import MerchantUser
from products.dtos.product_dto import ProductDto
from products.models.product import Product
from products.models.product_category import ProductCategory
from products.models.product_opition_group import ProductOptionGroup
from products.models.product_option import ProductOption


product_controller = APIRouter(prefix='/products', tags=['Product'])

class ProductController:
    
    @product_controller.get("/", response_model=Paginable[ProductDto])
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
            db: Session = Depends(get_db)):
        
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
            image: Optional[UploadFile] = None,
            images: Optional[List[UploadFile]] = None,
            current_user: MerchantUser = Depends(get_current_user),
            db: Session = Depends(get_db)):
        
        
        category: ProductCategory = db.query(ProductCategory).filter(ProductCategory.id == product_dto.category.id).first()
        if not category:
            raise HTTPException(status_code=401, detail="A Categoria não existe")
        product =  Product(
            **product_dto.model_dump(exclude=['category', 'option_groups']), 
            merchant_id=current_user.merchant_id, category_id=category.id
            )
        
        for group_dto in product_dto.option_groups:
            option_group = ProductOptionGroup(
                **group_dto.model_dump(exclude=["options"]),
                product_id=product.id
            )
            db.add(option_group)

            for option_dto in group_dto.opitions:
                option = ProductOption(
                    **option_dto.model_dump(),
                    product_option_group_id=option_group.id
                )
                db.add(option)
        
        db.add(product)
        db.commit()
        db.refresh(product)
        
        
        return ProductDto.model_validate(product)
    