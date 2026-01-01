import pytest
import os
from dotenv import load_dotenv

# Load environment variables for API token
load_dotenv()
TOKEN = os.getenv("API_KEY")
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Test constants
TEST_CARD_NUMBER = "BT0-001"
TEST_DECK_NAME = "Test Deck"

# Shared state for cascading tests
deck_id = None
card_added_to_deck = False

@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_list_decks_initial(client):
    """
    Ensure that the decks endpoint returns a list and is reachable.
    """
    response = await client.get("/decks/", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_create_deck(client):
    """
    Create a new empty deck with a test name.
    Store the deck ID for subsequent tests.
    """
    global deck_id
    response = await client.post(
        "/decks/add",
        params={"name": TEST_DECK_NAME},
        headers=HEADERS
    )
    assert response.status_code == 200
    data = response.json()
    assert "deck_id" in data
    assert data["message"] == "Deck created successfully"
    deck_id = data["deck_id"]


@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_get_deck_cards_initial(client):
    """
    Verify that a newly created deck has no cards.
    """
    if deck_id is None:
        pytest.skip("Deck was not created in previous test")

    response = await client.get(f"/decks/{deck_id}/cards", headers=HEADERS)
    assert response.status_code == 404  # Should be empty initially


@pytest.mark.order(4)
@pytest.mark.asyncio
async def test_add_card_to_deck(client):
    """
    Add a test card to the deck and verify success.
    """
    global card_added_to_deck
    if deck_id is None:
        pytest.skip("Deck was not created in previous test")

    response = await client.post(
        f"/decks/{deck_id}/cards/add",
        params={"card_number": TEST_CARD_NUMBER, "quantity": 1},
        headers=HEADERS
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Card added to deck"
    card_added_to_deck = True


@pytest.mark.order(5)
@pytest.mark.asyncio
async def test_get_deck_cards_after_add(client):
    """
    Verify that the card was added and quantity is correct.
    """
    if deck_id is None or not card_added_to_deck:
        pytest.skip("Previous tests did not complete successfully")

    response = await client.get(f"/decks/{deck_id}/cards", headers=HEADERS)
    assert response.status_code == 200
    cards = response.json()
    card = next((c for c in cards if c["card_number"] == TEST_CARD_NUMBER), None)
    assert card is not None
    assert card["quantity"] == 1


@pytest.mark.order(6)
@pytest.mark.asyncio
async def test_update_card_quantity(client):
    """
    Update the card quantity to a specific value and verify.
    """
    if deck_id is None or not card_added_to_deck:
        pytest.skip("Previous tests did not complete successfully")

    response = await client.put(
        f"/decks/{deck_id}/cards/update/{TEST_CARD_NUMBER}",
        params={"quantity": 5},
        headers=HEADERS
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Card quantity updated"

    # Verify quantity update
    response_check = await client.get(f"/decks/{deck_id}/cards", headers=HEADERS)
    card = next((c for c in response_check.json() if c["card_number"] == TEST_CARD_NUMBER), None)
    assert card["quantity"] == 5


@pytest.mark.order(7)
@pytest.mark.asyncio
async def test_remove_card_from_deck(client):
    """
    Remove the test card from the deck completely.
    """
    if deck_id is None:
        pytest.skip("Deck was not created in previous test")

    response = await client.delete(f"/decks/{deck_id}/cards/delete/{TEST_CARD_NUMBER}", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["message"] == "Card removed from deck"

    # Verify card is removed
    response_check = await client.get(f"/decks/{deck_id}/cards", headers=HEADERS)
    assert response_check.status_code == 404


@pytest.mark.order(8)
@pytest.mark.asyncio
async def test_invalid_parameters(client):
    """
    Verify that invalid input parameters are handled with proper errors.
    """
    if deck_id is None:
        pytest.skip("Deck was not created in previous test")

    # Invalid quantity (negative)
    resp1 = await client.put(
        f"/decks/{deck_id}/cards/update/{TEST_CARD_NUMBER}",
        params={"quantity": -1},
        headers=HEADERS
    )
    assert resp1.status_code == 422

    # Missing card_number when adding
    resp2 = await client.post(
        f"/decks/{deck_id}/cards/add",
        params={"quantity": 1},
        headers=HEADERS
    )
    assert resp2.status_code == 422

    # Invalid deck_id
    resp3 = await client.get(f"/decks/999999/cards", headers=HEADERS)
    assert resp3.status_code == 404
