import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.utils import get_openapi
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
security = HTTPBearer()


async def api_key_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


def custom_openapi(app):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["components"] = {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
    }

    if "paths" in openapi_schema:
        for path_item in openapi_schema["paths"].values():
            for operation in path_item.values():
                operation.setdefault("security", [])
                operation["security"].append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema
