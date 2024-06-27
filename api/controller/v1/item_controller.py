from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import UUID4
from sqlalchemy.orm import Session
from api.config.pagination import PaginationResponse, paginate
from api.domain.catalog.models.category import Category
from api.domain.catalog.models.item_context_modifier import ItemContextModifier
from api.domain.catalog.models.item_option_group import ItemOptionGroup
from api.domain.catalog.models.item_shift import ItemShift
from api.domain.catalog.models.price import Price
from api.domain.catalog.models.product import Product
from api.domain.catalog.dtos.item_dto import FullItemDto
from api.domain.catalog.models.item import Item
from api.domain.catalog.models.option_group import OptionGroup
from api.services.database_service import get_db
from api.services.security.auth_service import permission_dependency
from api.domain.merchant.dtos.merchant_user_dto import MerchantUserDto
from api.domain.merchant.models.merchant_permission import MerchantPermission

item_controller = APIRouter(prefix='/items', tags=['Catalog'])

@item_controller.get("/", response_model=PaginationResponse[FullItemDto])
async def get_items(
    page: int = 1,
    page_size: int = 20,
    merchant_user: MerchantUserDto = Depends(permission_dependency(MerchantPermission.CATALOG)),
    db: Session = Depends(get_db),
    ):
    items = db.query(Item).filter(Item.merchant_id == merchant_user.merchant.id).all()
    items_dto = [FullItemDto.model_validate(item) for item in items]
    return paginate(items_dto, page, page_size)


@item_controller.post("/", response_model=FullItemDto, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_data: FullItemDto,
    merchant_user: MerchantUserDto = Depends(permission_dependency(MerchantPermission.CATALOG)),
    db: Session = Depends(get_db),
    ):

    product = db.query(Product).filter_by(id=item_data.product.id, merchant_id=merchant_user.merchant.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    category = db.query(Category).filter_by(id=item_data.category.id, merchant_id=merchant_user.merchant.id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    item = Item(
        **item_data.model_dump(exclude=set(['price', 'shifts', 'context_modifiers', 'option_groups'])),
        merchant_id=merchant_user.merchant.id
    )
    db.add(item)
    db.commit()
    db.refresh(item)

    if item_data.price:
        price = Price(**item_data.price.model_dump(), item_id=item.id)
        db.add(price)

    for shift_data in item_data.shifts or []:
        shift = ItemShift(**shift_data, item_id=item.id)
        db.add(shift)

    for context_modifier_data in item_data.context_modifiers or []:
        context_modifier = ItemContextModifier(**context_modifier_data.model_dump(), item_id=item.id)
        db.add(context_modifier)

    for option_group_dto in item_data.option_groups or []:
        option_group: OptionGroup | None = db.query(OptionGroup).get(option_group_dto.id)
        if option_group:
            association = ItemOptionGroup(
                option_group_id = option_group.id,
                item_id = item.id
            )
            db.add(association)
            db.commit()
            db.refresh(association)

    db.commit()

    return FullItemDto.model_validate(item)


@item_controller.get("/{item_id}", response_model=FullItemDto)
async def get_item(
    item_id: UUID4,
    merchant_user: MerchantUserDto = Depends(permission_dependency(MerchantPermission.CATALOG)),
    db: Session = Depends(get_db),
):
    item = db.query(Item).filter(
        Item.id == item_id, Item.merchant_id == merchant_user.merchant.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return FullItemDto.model_validate(item)

@item_controller.put("/{item_id}", response_model=FullItemDto)
async def update_item(
    item_id: UUID4,
    item_data: FullItemDto,
    merchant_user: MerchantUserDto = Depends(permission_dependency(MerchantPermission.CATALOG)),
    db: Session = Depends(get_db),
    ):
    item = db.query(Item).filter(
        Item.id == item_id, Item.merchant_id == merchant_user.merchant.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    for attr, value in item_data.model_dump(exclude_unset=True).items():
        setattr(item, attr, value)

    db.commit()
    return FullItemDto.model_validate(item)

@item_controller.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: UUID4,
    merchant_user: MerchantUserDto = Depends(permission_dependency(MerchantPermission.CATALOG)),
    db: Session = Depends(get_db),
):
    item = db.query(Item).filter(
        Item.id == item_id, Item.merchant_id == merchant_user.merchant.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    db.delete(item)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



