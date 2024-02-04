from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from catalog.dtos.catalog_dto import CatalogDTO, CatalogItemDTO
from catalog.models.catalog import Catalog
from catalog.models.catalog_item import CatalogItem
from config.authorization.auth import get_current_user
from config.database import get_db
from merchants.models.merchant_user import MerchantUser


catalog_router = APIRouter(prefix='/catalog', tags=['Catalog'])

class CatalogController:
    
    @catalog_router.get("/{catalog_id}", response_model=CatalogDTO)
    async def get_catalog_by_id(
            catalog_id: int, 
            db: Session = Depends(get_db)
            ):
        catalog =  db.query(Catalog).filter(Catalog.id == catalog_id).first()
        if not catalog:
            raise HTTPException(status_code=404, detail="Inválid merchant or no products")
        return CatalogDTO.model_validate(catalog)
    
    @catalog_router.get("/{catalog_id}/item/{item_id}", response_model=CatalogItemDTO)
    async def get_menu_product(
            catalog_id: int, 
            catalog_item_id:int,
            db: Session = Depends(get_db)):
        
        catalog_item =  db.query(CatalogItem).filter(CatalogItem.catalog_id == catalog_id, CatalogItem.id == catalog_item_id).first()
        if not catalog_item:
            raise HTTPException(status_code=404, detail="Catalog item not found")
        return CatalogItemDTO.model_validate(catalog_item)
    
    

    @catalog_router.get("/", response_model=CatalogDTO)
    async def get_catalog_by_id(
            user:MerchantUser = Depends(get_current_user), 
            db: Session = Depends(get_db)
            ):
        catalogs =  db.query(Catalog).filter(Catalog.merchant_id == user.merchant_id).all()
        if not catalogs:
            raise HTTPException(status_code=404, detail="Inválid merchant or no products")
        catalogs = [CatalogDTO.model_validate(catalog) for catalog in catalogs]
        return catalogs
    
    @catalog_router.put("/{catalog_id}", response_model=CatalogDTO)
    async def update_merchant_user(
            catalog_id:int,
            catalog_dto:CatalogDTO,
            user: MerchantUser = Depends(get_current_user),
            db: Session = Depends(get_db)) -> CatalogDTO:
        
        catalog =  db.query(Catalog).filter(Catalog.id == catalog_id, Catalog.merchant_id == user.merchant_id).first()
        if not catalog:
            raise HTTPException(status_code=404, detail="Product not found")
        
        for key, value in catalog_dto.model_dump().items():
            setattr(catalog, key, value)
      
        db.commit()
        
        return CatalogDTO.model_validate(catalog)
    
    @catalog_router.post("/", response_model=CatalogDTO)
    async def create_catalog(
            catalog_dto:CatalogDTO,
            user: MerchantUser = Depends(get_current_user),
            db: Session = Depends(get_db)) -> CatalogDTO:
        
        
        new_catalog = Catalog(
            name=catalog_dto.name,
            description=catalog_dto.description,
            merchant_id=user.merchant_id
        )
        db.add(new_catalog)
        db.commit()
        db.refresh(new_catalog)

        items = []
        for item_dto in catalog_dto.items:
            product_id = item_dto.product.id 
            new_item = CatalogItem(catalog_id=new_catalog.id, product_id=product_id)
            items.append(new_item)

        db.add_all(items)
        db.commit()

        return CatalogDTO.model_validate(new_catalog)
    
   