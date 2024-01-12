from fastapi.testclient import TestClient
from fastapi import status
from main import app 
import random

client = TestClient(app)

def test_create_merchant():

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
            "email": f"{random.random()}@example.com",
            "name": "Test User",
            "phone": "123456789",
            "password": "securepassword",
        },
    }

    # Faça uma chamada para o endpoint de criação de merchant
    response = client.post("/auth/merchants/new/", json=test_merchant_data)

    # Verifique se a resposta é bem-sucedida (código 200)
    assert response.status_code == 200

    # Verifique se a resposta tem a estrutura esperada
    assert "access_token" in response.json()
    assert "merchant" in response.json()
    
    headers = {"Authorization": f"Bearer {response.json()['access_token']}"}

    
    response = client.delete("/merchants/final/delete", headers=headers)
    
    assert response.status_code == status.HTTP_200_OK

    
    