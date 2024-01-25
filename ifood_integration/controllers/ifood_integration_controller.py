from fastapi import APIRouter, Depends
from httpx import AsyncClient
from config.authorization.auth import get_current_admin_user
from config.database import get_db
from config.ifood import get_rotafood_acess_token
from ifood_integration.dtos.ifood_order_detail import IFoodOrderDetailDto
from ifood_integration.models.ifood_order import IFoodOrder
from merchants.controllers.authentication_controller import get_token_ifood
from merchants.models.merchant_user import MerchantUser

ifood_controller = APIRouter(prefix="/ifood_integration", tags=['IFoodIntegration'])


@ifood_controller.post('/get_orders/')


async def ifood_integration_create_get_merchant(
    user: MerchantUser = Depends(get_current_admin_user),
    db = Depends(get_db)
    ):
    url = ''
    async with AsyncClient() as client:
            response = await client.post(url, data={}, timeout=600)
    pass

async def ifood_integration_create_get_catalogs(
    user: MerchantUser = Depends(get_current_admin_user),
    db = Depends(get_db)
    ):
    url = ''
    async with AsyncClient() as client:
            response = await client.post(url, data={}, timeout=600)
    pass

async def ifood_integration_get_orders(
    user: MerchantUser = Depends(get_current_admin_user),
    db = Depends(get_db)
    ):
    url = 'https://merchant-api.ifood.com.br/order/v1.0/events:polling'
    headers = {"Authorization": f"bearer {get_rotafood_acess_token()}"}
    async with AsyncClient() as client:
            response = await client.post(url, headers=headers, timeout=600)
    if response.status_code == 200:
        orders = response.json()
        orders = [IFoodOrderDetailDto(**order) for order in orders]
        orders_db = [IFoodOrder(
            ifood_order_id=order.id,
            
            ) for order in orders]
    pass

