import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from api import cards, auxiliary, collection, decks
from core.middleware import CacheControlMiddleware
from core.security import custom_openapi, api_key_auth

load_dotenv()

app = FastAPI(
    title="Digimon Card API",
    description="API for managing Digimon cards, collections, and decks",
    version="1.0.0",
    openapi_tags=[
        {"name": "Cards", "description": "Endpoints for retrieving card information"},
        {
            "name": "Auxiliary Tables",
            "description": "Endpoints for card metadata and attributes",
        },
        {
            "name": "Collection",
            "description": "Endpoints for managing user card collections",
        },
        {"name": "Decks", "description": "Endpoints for managing card decks"},
    ],
)

# Middleware
app.add_middleware(CacheControlMiddleware)

# Routers with global security dependency
app.include_router(cards.router, dependencies=[Depends(api_key_auth)])
app.include_router(auxiliary.router, dependencies=[Depends(api_key_auth)])
app.include_router(collection.router, dependencies=[Depends(api_key_auth)])
app.include_router(decks.router, dependencies=[Depends(api_key_auth)])

# Custom OpenAPI with security
app.openapi = lambda: custom_openapi(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
