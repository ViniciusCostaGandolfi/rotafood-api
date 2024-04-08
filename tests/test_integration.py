from typing import List
from fastapi.testclient import TestClient
from domain.addresses.dtos.address_dto import AddressDto
from main import app 
import random
from pytest import fixture
from domain.orders.dtos.order_dto import OrderDto, OrderDeliveryDto, OrderDeliveredBy, OrderItemDto
from domain.orders.models import order_delivery
from domain.orders.models.order import OrderType
from domain.products.dtos.product_dto import CategoryDto, ProductDto
from domain.products.models.product import ProductType
from datetime import datetime

client = TestClient(app)

@fixture
def token_header():
    test_merchant_data = {
        "name": "Test Merchant",
        "documentType": "CNPJ",
        "document": "12345678901",
        "address": {
            "streetName": "Rua Teste",
            "formattedAddress": "Rua Teste, 123",
            "streetNumber": "123",
            "city": "Cidade Teste",
            "postalCode": "12345-678",
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
    assert "accessToken" in response.json()
    assert "merchant" in response.json()
    
    return {"Authorization": f"Bearer {response.json()['accessToken']}"}

def test_token_header(token_header):
    assert "Authorization" in token_header

@fixture
def category(token_header):
    # Create a new category
    category_data = {"name": "TestCategory", "description": "Test Description"}
    response = client.post("/category/", headers=token_header, json=category_data)
    assert response.status_code == 200

    return CategoryDto(**response.json())

def test_category(category):
    assert category.name == "TestCategory"

@fixture
def products(token_header, category:CategoryDto):
    products = []

    for i in range(20):
        product_data = {
           
            "name": f"TestProduct-{i}",
            "description": "Test Product Description",
            "weightQuantity": random.uniform(100, 1000),
            "weightUnit": "g",
            "volume": random.uniform(5, 11),
            "price": random.uniform(10, 30),
            "productType": ProductType.REGULAR.value,
            "category": category.model_dump(),
        }
        
        # Create a new product
        response = client.post("/products/", headers=token_header, json=product_data)
        assert response.status_code == 200

        products.append(ProductDto(**response.json()))
        
    return products

def test_products(products):
    assert len(products) == 20

@fixture
def orders(token_header, products: List[ProductDto]):
    orders = []
    for i in range(50):
        address = AddressDto(
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
         
        delivery = OrderDeliveryDto(
            pickup_code= "string", 
            delivered_by="MERCHANT", 
            address=address
        )
        num_indices = random.randint(1, 4)
        selected_indices = random.sample(range(len(products)), num_indices)
        selected_products = [OrderItemDto(
            quantity=1, 
            total_price=products[i].price, 
            total_volume=products[i].volume, 
            product=products[i]) for i in selected_indices]
        order = OrderDto(
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
        

def test_create_orders(orders: List[OrderDto]):
    assert len(orders) == 50
    
    
def test_ms_routes(token_header, orders):
    response = client.post("/routes/", headers=token_header)
    print(response.status_code)
    assert response.status_code == 200
