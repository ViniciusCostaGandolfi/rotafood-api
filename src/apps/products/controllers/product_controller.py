import base64
import io
import uuid
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
from configs.authorization.auth import get_current_user
from database import get_db
from configs.helpers import Paginable, paginate
from minio_bucket import upload_image_minio
from merchants.models.merchant_user import MerchantUser
from products.dtos.product_dto import ProductDto
from products.models.product import Product
from products.models.product_category import ProductCategory
from products.models.product_opition_group import ProductOptionGroup
from products.models.product_option import ProductOption
from PIL import Image



product_controller = APIRouter(prefix='/products', tags=['Product'])


@product_controller.get("/", response_model=Paginable[ProductDto])
async def get_products(
        page: int = 1,
        page_size: int = 10,
        current_user: MerchantUser = Depends(get_current_user),
        db: Session = Depends(get_db)
        ):
    products_db =  db.query(Product).filter(Product.merchant_id == current_user.merchant_id).all()
    if not products_db:
        raise HTTPException(status_code=401, detail="No products")
    
    data = [ProductDto.model_validate(product) for product in products_db]
                
    return paginate(data, page, page_size)

@product_controller.get("/{product_id}", response_model=ProductDto)
async def get_product_by_id(
        product_id:int,
        db: Session = Depends(get_db)):
    
    product =  db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="No product with this")
    return ProductDto.model_validate(product)


@product_controller.put("/{product_id}", response_model=ProductDto)
async def update_product_by_id(
        product_id,
        product_dto: ProductDto,
        current_user: MerchantUser = Depends(get_current_user),
        db: Session = Depends(get_db)):
    
    product_db: Product | None =  db.query(Product).filter(Product.id == product_id, Product.merchant_id == current_user.merchant_id).first()
    
    if not product_db:
        raise HTTPException(status_code=404, detail="No product with this")
    
    if product_dto.image and product_dto.image:
        image_url = upload_image_minio(product_dto.image)
        product_db.image = image_url
            
                
    if product_dto.category:
        category: ProductCategory = db.query(ProductCategory).filter(ProductCategory.id == product_dto.category.id).first()
        if not category:
            raise HTTPException(status_code=401, detail="A Categoria não encontrada")
        product_db.category_id = category.id
        
    for key, value in product_dto.model_dump(exclude=['category', 'option_groups', 'image', 'multiple_images']).items():
        setattr(product_db, key, value)    
    
    
    for group_dto in product_dto.option_groups:
        option_group = db.query(ProductOptionGroup).filter(
            ProductOptionGroup.id == group_dto.id, 
            ProductOptionGroup.product_id == product_id
        ).first()
        if option_group:
            update_data = group_dto.model_dump( exclude=["options"])
            for key, value in update_data.items():
                setattr(option_group, key, value)
        else:
            option_group = ProductOptionGroup(
                **group_dto.model_dump(exclude=["options"]),
                product_id=product_dto.id
            )
            db.add(option_group)
            db.commit()
            for option_dto in group_dto.opitions:
                option = ProductOption(
                    **option_dto.model_dump(exclude=['image_path']),
                    product_option_group_id=option_group.id
                )
                if option.image_path:
                    image_url = upload_image_minio(option.image_path)
                    option.image_path = image_url
                db.add(option)
                db.commit()
    
    db.refresh(product_db)
    
    return ProductDto.model_validate(product_db)

@product_controller.post("/", response_model=ProductDto)
async def create_product(
        product: ProductDto,
        current_user: MerchantUser = Depends(get_current_user),
        db: Session = Depends(get_db)):
    
    product_db =  Product(
        **product.model_dump(exclude=['category', 'option_groups', 'image', 'multiple_images']), 
        merchant_id=current_user.merchant_id,
        )
    
    if product.image:
        image_url = upload_image_minio(product.image)
        product_db.image = image_url
            
                
    if product.category:
        category: ProductCategory = db.query(ProductCategory).filter(ProductCategory.id == product.category.id).first()
        if not category:
            raise HTTPException(status_code=401, detail="A Categoria não encontrada")
        product_db.category_id = category.id
    
    
    
    db.add(product_db)
    db.commit()
    
    for group_dto in product.option_groups:
        option_group = ProductOptionGroup(
            **group_dto.model_dump(exclude=["options"]),
            product_id=product.id
        )
        db.add(option_group)
        db.commit()

        for option_dto in group_dto.opitions:
            option = ProductOption(
                **option_dto.model_dump(exclude=['image_path']),
                product_option_group_id=option_group.id
            )
            if option.image_path:
                image_url = upload_image_minio(option.image_path)
                option.image_path = image_url
            db.add(option)
            db.commit()
    
    db.refresh(product_db)
    
    return ProductDto.model_validate(product_db)
