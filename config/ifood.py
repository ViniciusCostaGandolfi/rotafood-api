import asyncio
from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
import httpx
from dotenv import load_dotenv

load_dotenv()

IFOOD_GRANT_TYPE = os.getenv("IFOOD_GRANT_TYPE")
IFOOD_CLIENT_ID = os.getenv("IFOOD_CLIENT_ID")
IFOOD_CLIENT_SECRET = os.getenv("IFOOD_CLIENT_SECRET")

rotafoodAccessToken, expiresIn = '', 1

async def get_rotafood_acess_token():
    global rotafoodAccessToken, expiresIn
    current_time = asyncio.get_event_loop().time()

    if current_time > expiresIn:
        print("Token expirado, renovando...")
        url = "https://merchant-api.ifood.com.br/authentication/v1.0/oauth/token"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data={
                "grantType": IFOOD_GRANT_TYPE,
                "clientId": IFOOD_CLIENT_ID,
                "clientSecret": IFOOD_CLIENT_SECRET,
            }, timeout=600)

        if response.status_code == 200:
            data = response.json()
            rotafoodAccessToken = data["accessToken"]
            expiresIn = current_time + float(data["expiresIn"] * 0.9)
            print("AccessToken renovado")
            print(f"{rotafoodAccessToken}")
        else:
            print(f"Falha ao renovar AccessToken, status_code: {response.status_code}")
    
    return rotafoodAccessToken

@asynccontextmanager
async def lifespan(app: FastAPI):
    global rotafoodAccessToken, expiresIn
    rotafoodAccessToken, expiresIn = await get_rotafood_acess_token()
    yield
