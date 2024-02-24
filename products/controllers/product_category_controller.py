from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List, Optional
from config.authorization.auth import get_current_user, permission_dependency
from config.database import get_db
from merchants.models.merchant_user import MerchantUser, ModulePermissions
from products.dtos.product_dto import CategoryDto, SearchCategoryDto
from products.models.product_category import ProductCategory


category_controller = APIRouter(prefix='/product_category', tags=['ProductCategory'])

@category_controller.get("/", response_model=List[CategoryDto])
async def get_product_categories(
        current_user: MerchantUser = Depends(
                    permission_dependency(
                        ModulePermissions.PRODUCTS
                        )
                    ),
        id: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        db: Session = Depends(get_db)
        ):

    query =  db.query(ProductCategory).filter(ProductCategory.merchant_id == current_user.merchant_id)
    if id is not None:
        query = query.filter(ProductCategory.id == id)
    if name is not None:
        query = query.filter(ProductCategory.name.contains(name))
    if description is not None:
        query = query.filter(ProductCategory.description.contains(description))


    categories_db = query.all()
        
    return [CategoryDto.model_validate(category) for category in categories_db]

@category_controller.get("/{product_category_id}", response_model=CategoryDto)
async def get_product_category_by_id(
        product_category_id:int,
        current_user: MerchantUser = Depends(
                    permission_dependency(
                        ModulePermissions.PRODUCTS
                        )
                    ),
        db: Session = Depends(get_db)):
    
    category =  db.query(ProductCategory).filter(
        ProductCategory.id == product_category_id, 
        ProductCategory.merchant_id == current_user.merchant_id
        ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Sem categorias")
    return CategoryDto.model_validate(category)


@category_controller.patch("/{product_category_id}", response_model=CategoryDto)
async def update_product_category(
        product_category_id:int,
        category_dto:CategoryDto,
        current_user: MerchantUser = Depends(
                    permission_dependency(ModulePermissions.PRODUCTS)
                    ),
        db: Session = Depends(get_db)) -> CategoryDto:
    
    category =  db.query(ProductCategory).filter(
        ProductCategory.id == product_category_id,
        ProductCategory.merchant_id == current_user.merchant_id

        ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não existe")
    
    
    for key, value in category_dto.model_dump().items():
        if value is not None:
            setattr(category, current_user, key, value)
    
    db.commit()
    db.refresh(category)
    
    return CategoryDto.model_validate(category)



@category_controller.delete("/{product_category_id}")
async def delete_product_category(
        product_category_id:int,
        current_user: MerchantUser = Depends(
                    permission_dependency(ModulePermissions.PRODUCTS)
                    ),
        db: Session = Depends(get_db)) -> CategoryDto:
    
    category =  db.query(ProductCategory).filter(
        ProductCategory.id == product_category_id,
        ProductCategory.merchant_id == current_user.merchant_id
        ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(category)
    db.commit()
    
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@category_controller.post("/", response_model=CategoryDto)
async def create_product_category(
        category_dto:CategoryDto,
        current_user: MerchantUser = Depends(
                    permission_dependency(ModulePermissions.PRODUCTS)
                    ),
        db: Session = Depends(get_db)) -> CategoryDto:
    
    
    category = ProductCategory(**category_dto.model_dump(), merchant_id=current_user.merchant_id)
    db.add(category)
    db.commit()
    db.refresh(category)
    
    
    return CategoryDto.model_validate(category)