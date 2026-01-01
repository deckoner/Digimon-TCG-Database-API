import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from main import app
import pytest_asyncio


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
