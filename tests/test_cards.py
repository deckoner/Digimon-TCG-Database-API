import pytest
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
TOKEN = os.getenv("API_KEY")
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Test retrieving all cards (pagination removed)
@pytest.mark.asyncio
async def test_get_cards(client):
    response = await client.get(
        "/cards/",
        params={"include_alternative": True},
        headers=HEADERS,
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  # ahora esperamos todos los registros

    for card in data:
        assert "id" in card
        assert "card_number" in card
        assert "name" in card
        assert "card_type" in card
        assert "rarity" in card
        assert "color_one" in card
        assert "image_url" in card
        assert "bt_abbreviation" in card
        assert "alternative" in card

# Test retrieving full card details (pagination removed)
@pytest.mark.asyncio
async def test_get_cards_full(client):
    response = await client.get(
        "/cards/full/",
        params={"include_alternative": True},
        headers=HEADERS,
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  # ahora esperamos todos los registros

    for card in data:
        assert "id" in card
        assert "card_number" in card
        assert "name" in card
        assert "dp" in card
        assert "card_type" in card
        assert "rarity" in card
        assert "color_one" in card
        assert "image_url" in card
        assert "bt_abbreviation" in card
        assert "alternative" in card
        assert "evolution_effect" in card
        assert "effect" in card
        assert "security_effect" in card

# Test retrieving a single card by its number (sin cambios)
@pytest.mark.asyncio
async def test_get_card_by_number(client):
    card_number = "EX9-001"
    response = await client.get(f"/cards/{card_number}", headers=HEADERS)
    assert response.status_code == 200
    card = response.json()

    # Check all expected fields
    expected_fields = [
        "id", "card_number", "name", "dp", "card_type", "rarity",
        "color_one", "color_two", "color_three", "image_url", "cost",
        "stage", "attribute", "type_one", "type_two",
        "evolution_cost_one", "evolution_cost_two",
        "effect", "evolution_effect", "security_effect",
        "bt_abbreviation", "alternative"
    ]
    for field in expected_fields:
        assert field in card

# Test retrieving a card with alternative versions (sin cambios)
@pytest.mark.asyncio
async def test_get_card_alternatives_with_versions(client):
    card_number = "EX9-001"
    response = await client.get(f"/cards/{card_number}/alternatives", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    first = data[0]
    expected_fields = [
        "id", "card_number", "name", "dp", "card_type", "rarity",
        "color_one", "image_url", "bt_abbreviation", "alternative"
    ]
    for field in expected_fields:
        assert field in first

    if len(data) > 1:
        second = data[1]
        assert "id" in second
        assert "card_number" in second

# Test retrieving a card without alternative versions (sin cambios)
@pytest.mark.asyncio
async def test_get_card_alternatives_no_versions(client):
    card_number = "BT12-055"
    response = await client.get(f"/cards/{card_number}/alternatives", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1

    card = data[0]
    expected_fields = [
        "id", "card_number", "name", "dp", "card_type", "rarity",
        "color_one", "color_two", "color_three", "image_url", "cost",
        "stage", "attribute", "type_one", "type_two",
        "evolution_cost_one", "evolution_cost_two",
        "effect", "evolution_effect", "security_effect",
        "bt_abbreviation", "alternative"
    ]
    for field in expected_fields:
        assert field in card

# Test searching cards by name (sin cambios)
@pytest.mark.asyncio
async def test_search_cards_by_name(client):
    query = "DemiDevi"
    response = await client.get(f"/cards/search/?name_part={query}", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    for card in data:
        expected_fields = [
            "id", "card_number", "name", "dp", "card_type", "rarity",
            "color_one", "image_url", "bt_abbreviation", "alternative"
        ]
        for field in expected_fields:
            assert field in card

# Test searching cards including their alternative versions (sin cambios)
@pytest.mark.asyncio
async def test_search_cards_with_alternatives(client):
    query = "DemiDevi"
    response = await client.get(f"/cards/search-with-alternatives/?name_part={query}", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    for card in data:
        expected_fields = [
            "id", "card_number", "name", "dp", "card_type", "rarity",
            "color_one", "image_url", "bt_abbreviation", "alternatives"
        ]
        for field in expected_fields:
            assert field in card

        for alt in card["alternatives"]:
            alt_fields = ["id", "card_number", "name", "image_url", "alternative"]
            for field in alt_fields:
                assert field in alt

# Test retrieving all cards with IDs instead of names
@pytest.mark.asyncio
async def test_get_cards_with_ids(client):
    response = await client.get(
        "/cards/ids/",
        params={"include_alternative": True},
        headers=HEADERS,
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    for card in data:
        expected_fields = [
            "id", "card_number", "name",
            "card_type", "rarity",
            "color_one", "color_two", "color_three",
            "image_url", "cost", "stage",
            "attribute", "type_one", "type_two",
            "bt_abbreviation", "alternative"
        ]
        for field in expected_fields:
            assert field in card

        for fk_field in ["card_type", "rarity", "color_one", "color_two", "color_three",
                         "stage", "attribute", "type_one", "type_two", "bt_abbreviation"]:
            assert isinstance(card[fk_field], (int, type(None)))
