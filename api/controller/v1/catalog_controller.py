from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import UUID4
from sqlalchemy.orm import Session
from api.config.pagination import PaginationResponse, paginate
from api.domain.catalog.dtos.catalog_dto import CatalogDto, CatalogUpdateDto
from api.domain.catalog.models.catalog import Catalog
from api.domain.catalog.models.catalog_category import CatalogCategory
from api.services.database_service import get_db
from api.services.security.auth_service import permission_dependency
from api.domain.merchant.dtos.merchant_dto import MerchantDto
from api.domain.merchant.dtos.merchant_user_dto import MerchantUserDto
from api.domain.merchant.models.merchant_permission import MerchantPermission

catalog_controller = APIRouter(prefix='', tags=['Catalog'])


@catalog_controller.get("/catalogs")
async def get_catalogs(
        merchant_user: MerchantUserDto = Depends(permission_dependency(
            MerchantPermission.CATALOG
        )),
        db: Session = Depends(get_db),
        page: int = 1,
        page_size: int = 20,    
    ) -> PaginationResponse[CatalogDto]:

    catalogs: List[Catalog] = db.query(Catalog).filter(
        Catalog.merchant_id == merchant_user.merchant.id).all()
    if catalogs:
        catalogs_dto = [CatalogDto.model_validate(catalog) for catalog in catalogs]
        return paginate(catalogs_dto, page, page_size)
    raise HTTPException(401, detail="Catálogo não encontrado")

@catalog_controller.get("/catalogs/{catalog_id}")
async def get_catalog_by_id(
        catalog_id: UUID4,
        merchant_user: MerchantUserDto = Depends(permission_dependency(
            MerchantPermission.CATALOG
        )),
        db: Session = Depends(get_db)
    ) -> CatalogDto:

    catalog: Catalog | None = db.query(Catalog).filter(
        Catalog.merchant_id == merchant_user.merchant.id, Catalog.id == catalog_id).first()
    if catalog:
        return CatalogDto.model_validate(catalog)
    raise HTTPException(401, detail="Catálogo não encontrado")

@catalog_controller.post("/catalogs")
async def create_catalog(
        catalog_dto: CatalogUpdateDto,
        merchant_user: MerchantUserDto = Depends(permission_dependency(
            MerchantPermission.CATALOG
        )),
        db: Session = Depends(get_db)
    ) -> CatalogDto:

    catalog = Catalog(
        name=catalog_dto.name,
        modified_at=datetime.now(timezone.utc),
        catalog_context_modifier=catalog_dto.catalog_context_modifier,
        merchant_id=merchant_user.merchant.id 
    )
    db.add(catalog)
    db.commit()
    db.refresh(catalog)
    if catalog:
        return CatalogDto.model_validate(catalog)
    raise HTTPException(401, detail="Catálogo não encontrado")

@catalog_controller.get("/catalogs/{catalog_id}")
async def update_catalog_by_id(
        catalog_id: UUID4,
        catalog_dto: CatalogUpdateDto,
        merchant_user: MerchantUserDto = Depends(
        permission_dependency(MerchantPermission.CATALOG)
        ),
        db: Session = Depends(get_db)
    ) -> CatalogDto:

    catalog: Catalog | None = db.query(Catalog).filter(
        Catalog.merchant_id == merchant_user.merchant.id, Catalog.id == catalog_id).first()
    if catalog:
        for key, value in catalog_dto.model_dump(exclude=set(['id'])).items():
            if hasattr(catalog, key) and value is not None:
                setattr(catalog, key, value)
        db.commit()
        db.refresh(catalog)
        return CatalogDto.model_validate(catalog)
    raise HTTPException(401, detail="Catálogo não encontrado")


@catalog_controller.delete("/catalogs/{catalog_id}", status_code=204)
async def delete_category(
    catalog_id: UUID4,
    merchant_user: MerchantUserDto = Depends(permission_dependency(
        MerchantPermission.CATALOG
    )),
    db: Session = Depends(get_db),
):
    category = db.query(Catalog).join(CatalogCategory).filter(
        CatalogCategory.catalog_id == catalog_id,
        Catalog.id == catalog_id,
        Catalog.merchant_id == merchant_user.merchant.id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    db.query(CatalogCategory).filter(
        CatalogCategory.catalog_id == catalog_id, 
    ).delete()

    db.delete(category)
    db.commit()

    return Response(status_code=204)



