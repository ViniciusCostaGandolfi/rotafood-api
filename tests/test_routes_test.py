from typing import List
from fastapi.testclient import TestClient
from addresses.DTOs.address_dto import AddressDTO
from main import app 
import random
from pytest import fixture
from orders.DTOs.order_dto import OrderDTO, OrderDeliveryDTO, OrderDeliveredBy, OrderItemDTO
from orders.models import order_delivery
from orders.models.order import OrderType
from products.dtos.product_dto import CategoryDTO, ProductDTO
from products.models.product import ProductType
from datetime import datetime

client = TestClient(app)

    
    
def test_ms_routes():
    response = client.post("/routes/test/auto_generate/30/")
    print(response.status_code)
    print(f'\n\n\n{response.json()}\n\n\n')
    assert response.status_code == 200

