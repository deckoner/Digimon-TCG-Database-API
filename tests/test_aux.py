import pytest
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
TOKEN = os.getenv("API_KEY")
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# List of auxiliary endpoints to test for general collections
AUX_ENDPOINTS = [
    "/aux/colors",
    "/aux/card-types",
    "/aux/rarities",
    "/aux/stages",
    "/aux/attributes",
    "/aux/types",
]

# List of auxiliary endpoints that require an ID parameter and the expected key to check
AUX_ID_ENDPOINTS = [
    ("/aux/colors/{}", "name"),
    ("/aux/card-types/{}", "name"),
    ("/aux/rarities/{}", "name"),
    ("/aux/stages/{}", "name"),
    ("/aux/attributes/{}", "name"),
    ("/aux/types/{}", "name"),
]


# Test retrieving all BT sets
@pytest.mark.asyncio
async def test_bts_endpoint(client):
    response = await client.get("/aux/bts", headers=HEADERS)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    # Validate required fields in each BT set
    for item in data:
        assert "id" in item
        assert "name" in item
        assert "abbreviation" in item


# Test retrieving general auxiliary collections (colors, types, rarities, etc.)
@pytest.mark.asyncio
@pytest.mark.parametrize("endpoint", AUX_ENDPOINTS)
async def test_aux_endpoints(client, endpoint):
    response = await client.get(endpoint, headers=HEADERS)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    # Ensure each item contains an id and name
    for item in data:
        assert "id" in item
        assert "name" in item


# Test retrieving a specific BT set by ID
@pytest.mark.asyncio
async def test_bts_by_id(client):
    response = await client.get("/aux/bts/1", headers=HEADERS)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert data.get("id") == 1
    # Verify all required fields are present
    assert "name" in data
    assert "abbreviation" in data


# Test retrieving a specific auxiliary item by ID (colors, types, rarities, etc.)
@pytest.mark.asyncio
@pytest.mark.parametrize("endpoint_tpl, key", AUX_ID_ENDPOINTS)
async def test_aux_by_id(client, endpoint_tpl, key):
    url = endpoint_tpl.format(1)
    response = await client.get(url, headers=HEADERS)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    # Ensure the ID matches and expected key exists
    assert data.get("id") == 1
    assert key in data
