from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import UUID4
from sqlalchemy.orm import Session
from api.config.pagination import PaginationResponse, paginate
from api.domain.catalog.dtos.category_dto import CategoryDto, CategoryUpdateDto
from api.domain.catalog.models.catalog import Catalog
from api.domain.catalog.models.catalog_category import CatalogCategory
from api.domain.catalog.models.category import Category
from api.services.database_service import get_db
from api.services.security.auth_service import permission_dependency
from api.domain.merchant.dtos.merchant_user_dto import MerchantUserDto
from api.domain.merchant.models.merchant_permission import MerchantPermission

category_controller = APIRouter(prefix='', tags=['Catalog'])

@category_controller.get("/catalogs/{catalog_id}/categories", 
                         response_model=PaginationResponse[CategoryDto])
async def get_categories(
    catalog_id: UUID4, 
    page: int = 1, 
    page_size: int = 20,
    merchant_user: MerchantUserDto = Depends(permission_dependency(
        MerchantPermission.CATALOG
    )),
    db: Session = Depends(get_db)):
    categories = db.query(Category).join(CatalogCategory).filter(
        CatalogCategory.catalog_id == catalog_id, 
        Category.merchant_id == merchant_user.merchant.id).all()
    
    categories_dto = [CategoryDto.model_validate(category) for category in categories]
    return paginate(categories_dto, page, page_size)


@category_controller.post("/catalogs/{catalog_id}/categories", response_model=CategoryDto, status_code=201)
async def create_category(
    catalog_id: UUID4,
    category_data: CategoryUpdateDto,
    merchant_user: MerchantUserDto = Depends(permission_dependency(
        MerchantPermission.CATALOG
    )),
    db: Session = Depends(get_db),
):
    catalog = db.query(Catalog).filter(
        Catalog.id == catalog_id, 
        Catalog.merchant_id == merchant_user.merchant.id).first()
    if not catalog:
        raise HTTPException(status_code=404, detail="Catálogo não encontrado")

    category = Category(
        **category_data.model_dump(),
        merchant_id=merchant_user.merchant.id
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    catalog_category = CatalogCategory(catalog_id=catalog_id, category_id=category.id)
    db.add(catalog_category)
    db.commit()

    return CategoryDto.model_validate(category)


@category_controller.get("/catalogs/{catalog_id}/categories/{category_id}", response_model=CategoryDto)
async def get_category(
    catalog_id: UUID4, 
    category_id: UUID4, 
    merchant_user: MerchantUserDto = Depends(permission_dependency(
        MerchantPermission.CATALOG
    )),
    db: Session = Depends(get_db)):
    category = db.query(Category).join(CatalogCategory).filter(
        CatalogCategory.catalog_id == catalog_id,
        Category.id == category_id,
        Category.merchant_id == merchant_user.merchant.id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return CategoryDto.model_validate(category)


@category_controller.put("/catalogs/{catalog_id}/categories/{category_id}", response_model=CategoryDto)
async def update_category(
    catalog_id: UUID4,
    category_id: UUID4,
    category_data: CategoryUpdateDto,
    merchant_user: MerchantUserDto = Depends(permission_dependency(
        MerchantPermission.CATALOG
    )),
    db: Session = Depends(get_db),
):
    category = db.query(Category).join(CatalogCategory).filter(
        CatalogCategory.catalog_id == catalog_id,
        Category.id == category_id,
        Category.merchant_id == merchant_user.merchant.id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    for attr, value in category_data.model_dump(exclude=set(['id'])).items():
        setattr(category, attr, value)

    db.commit()
    return CategoryDto.model_validate(category)

@category_controller.delete("/catalogs/{catalog_id}/categories/{category_id}", status_code=204)
async def delete_category(
    catalog_id: UUID4,
    category_id: UUID4,
    merchant_user: MerchantUserDto = Depends(permission_dependency(
        MerchantPermission.CATALOG
    )),
    db: Session = Depends(get_db),
):
    category = db.query(Category).join(CatalogCategory).filter(
        CatalogCategory.catalog_id == catalog_id,
        Category.id == category_id,
        Category.merchant_id == merchant_user.merchant.id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    db.query(CatalogCategory).filter(
        CatalogCategory.catalog_id == catalog_id, 
        CatalogCategory.category_id == category_id,
    ).delete()

    db.delete(category)
    db.commit()

    return Response(status_code=204)



