from fastapi.testclient import TestClient
from main import app 


client = TestClient(app)

    
    
def test_ms_routes():
    response = client.post("/routes/test/auto_generate/30/")
    assert response.status_code == 200

