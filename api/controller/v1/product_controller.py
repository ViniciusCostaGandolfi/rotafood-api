from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import UUID4
from sqlalchemy.orm import Session
from api.config.pagination import PaginationResponse, paginate
from api.domain.catalog.dtos.product_dto import ProductCreateDto, ProductDto, ProductUpdateDto
from api.domain.catalog.models.product import Product
from api.services.database_service import get_db
from api.services.security.auth_service import permission_dependency
from api.domain.merchant.dtos.merchant_user_dto import MerchantUserDto
from api.domain.merchant.models.merchant_permission import MerchantPermission

product_controller = APIRouter(prefix='/products', tags=['Product']) 

@product_controller.get("/", response_model=PaginationResponse[ProductDto])
async def get_products(
    page: int = 1, 
    page_size: int = 20,
    merchant_user: MerchantUserDto = Depends(permission_dependency(
        MerchantPermission.CATALOG
    )),
    db: Session = Depends(get_db)):
    products = db.query(Product).filter(
        Product.merchant_id == merchant_user.merchant.id
    ).all()
    
    products_dto = [ProductDto.model_validate(product) for product in products]
    return paginate(products_dto, page, page_size)


@product_controller.post("/", status_code=201)
async def create_product(
    product_data: ProductCreateDto,
    merchant_user: MerchantUserDto = Depends(permission_dependency(
        MerchantPermission.CATALOG
    )),
    db: Session = Depends(get_db),
):
    product = Product(
        **product_data.dict(),
        merchant_id=merchant_user.merchant.id
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return ProductDto.model_validate(product)


@product_controller.get("/{product_id}")
async def get_product(
    product_id: UUID4, 
    merchant_user: MerchantUserDto = Depends(permission_dependency(
        MerchantPermission.CATALOG
    )),
    db: Session = Depends(get_db)) -> ProductDto:
    product = db.query(Product).filter(
        Product.id == product_id, 
        Product.merchant_id == merchant_user.merchant.id
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return ProductDto.model_validate(product)


@product_controller.put("/{product_id}")
async def update_product(
    product_id: UUID4,
    product_data: ProductUpdateDto,
    merchant_user: MerchantUserDto = Depends(permission_dependency(
        MerchantPermission.CATALOG
    )),
    db: Session = Depends(get_db)) -> ProductDto:
    product = db.query(Product).filter(
        Product.id == product_id, 
        Product.merchant_id == merchant_user.merchant.id
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    for attr, value in product_data.dict(exclude_unset=True).items():
        setattr(product, attr, value)

    db.commit()
    return ProductDto.model_validate(product)


@product_controller.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: UUID4,
    merchant_user: MerchantUserDto = Depends(permission_dependency(
        MerchantPermission.CATALOG
    )),
    db: Session = Depends(get_db)) -> Response:
    product = db.query(Product).filter(
        Product.id == product_id, 
        Product.merchant_id == merchant_user.merchant.id
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db.delete(product)
    db.commit()

    return Response(status_code=204)
