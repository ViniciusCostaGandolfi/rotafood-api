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

@fixture
def token_header():
    test_merchant_data = {
        "name": "Test Merchant",
        "document_type": "CNPJ",
        "document": "12345678901",
        "address": {
            "street_name": "Rua Teste",
            "formatted_address": "Rua Teste, 123",
            "street_number": "123",
            "city": "Cidade Teste",
            "postal_code": "12345-678",
            "neighborhood": "Bairro Teste",
            "state": "Estado Teste",
            "complement": "Complemento Teste",
            "latitude": 0.0,
            "longitude": 0.0,
        },
        "user": {
            "email": f"{random.random()}_{random.random()}@example.com",
            "name": "Test User",
            "phone": "123456789",
            "password": "securepassword",
        },
    }
    
    response = client.post("/auth/merchants/new/", json=test_merchant_data)

    # Verifique se a resposta é bem-sucedida (código 200)
    assert response.status_code == 200

    # Verifique se a resposta tem a estrutura esperada
    assert "access_token" in response.json()
    assert "merchant" in response.json()
    
    return {"Authorization": f"Bearer {response.json()['access_token']}"}

def test_token_header(token_header):
    assert "Authorization" in token_header

@fixture
def category(token_header):
    # Create a new category
    category_data = {"name": "TestCategory", "description": "Test Description"}
    response = client.post("/category/", headers=token_header, json=category_data)
    assert response.status_code == 200

    return CategoryDTO(**response.json())

def test_category(category):
    assert category.name == "TestCategory"

@fixture
def products(token_header, category:CategoryDTO):
    products = []

    for i in range(20):
        product_data = {
           
            "name": f"TestProduct-{i}",
            "description": "Test Product Description",
            "weight_quantity": random.uniform(100, 1000),
            "weight_unit": "g",
            "volume": random.uniform(5, 11),
            "price": random.uniform(10, 30),
            "product_type": ProductType.REGULAR.value,
            "category": category.model_dump(),
        }
        
        # Create a new product
        response = client.post("/products/", headers=token_header, json=product_data)
        assert response.status_code == 200

        products.append(ProductDTO(**response.json()))
        
    return products

def test_products(products):
    assert len(products) == 20

@fixture
def orders(token_header, products: List[ProductDTO]):
    orders = []
    for i in range(50):
        address = AddressDTO(
            street_name="string",
            formatted_address="string",
            street_number="string",
            city="string",
            postal_code="string",
            neighborhood="string",
            state="string",
            complement="string",
            latitude=random.uniform(-90, 90),
            longitude=random.uniform(-90, 90)

        )
         
        delivery = OrderDeliveryDTO(
            pickup_code= "string", 
            delivered_by="MERCHANT", 
            address=address
        )
        num_indices = random.randint(1, 4)
        selected_indices = random.sample(range(len(products)), num_indices)
        selected_products = [OrderItemDTO(
            quantity=1, 
            total_price=products[i].price, 
            total_volume=products[i].volume, 
            product=products[i]) for i in selected_indices]
        order = OrderDTO(
            total_volume=10,
            total_price=10,
            order_type=OrderType.DELIVERY.value,
            delivery=delivery,
            items=selected_products
        )
        response = client.post("/orders/", headers=token_header, content=order.model_dump_json())
        assert response.status_code == 200
        
        orders.append(order)
        
    return orders
        

def test_create_orders(orders: List[OrderDTO]):
    assert len(orders) == 50
    
    
def test_ms_routes(token_header, orders):
    response = client.post("/routes/", headers=token_header)
    print(response.status_code)
    print(f'\n\n\n{response.json()}\n\n\n')
    assert response.status_code == 200
