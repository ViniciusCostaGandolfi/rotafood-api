from fastapi.testclient import TestClient
from fastapi import status
from main import app 
import random

client = TestClient(app)

def test_create_merchant():

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
            "email": f"{random.random()}@example.com",
            "name": "Test User",
            "phone": "123456789",
            "password": "securepassword",
        },
    }

    # Faça uma chamada para o endpoint de criação de merchant
    response = client.post("/auth/merchants/new/", json=test_merchant_data)
    
    print(response)

    # Verifique se a resposta é bem-sucedida (código 200)
    assert response.status_code == 200

    # Verifique se a resposta tem a estrutura esperada
    assert "accessToken" in response.json()
    assert "merchant" in response.json()
    
    headers = {"Authorization": f"Bearer {response.json()['accessToken']}"}

    
    response = client.delete("/merchants/final/delete", headers=headers)
    
    assert response.status_code == status.HTTP_200_OK

    
    