import pytest
import os
from dotenv import load_dotenv

# Load environment variables and extract API token
load_dotenv()
TOKEN = os.getenv("API_KEY")
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Card number used as a test fixture across all cases
TEST_CARD_NUMBER = "BT0-001"

# Shared state to coordinate test dependencies
card_added = False


@pytest.mark.order(1)
@pytest.mark.asyncio
async def test_cleanup_before_start(client):
    """
    Ensures the target card is not present in the collection before tests run.
    This creates a clean, predictable starting point for the test suite.
    """
    await client.delete(f"/collection/delete/{TEST_CARD_NUMBER}", headers=HEADERS)


@pytest.mark.order(2)
@pytest.mark.asyncio
async def test_add_card(client):
    """
    Adds a single card to the collection and confirms the operation succeeded.
    Sets a flag used by subsequent tests.
    """
    global card_added

    response = await client.post(
        "/collection/add",
        params={"card_number": TEST_CARD_NUMBER, "quantity": 1},
        headers=HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Card added to collection"

    card_added = True


@pytest.mark.order(3)
@pytest.mark.asyncio
async def test_card_appears(client):
    """
    Checks that the recently added card is present in the user's collection
    with the expected quantity.
    """
    if not card_added:
        pytest.skip("Card was not added successfully in the previous test.")

    response = await client.get("/collection/", headers=HEADERS)
    assert response.status_code == 200

    cards = response.json()
    card = next((c for c in cards if c["card_number"] == TEST_CARD_NUMBER), None)

    assert card is not None
    assert card["quantity"] == 1


@pytest.mark.order(4)
@pytest.mark.asyncio
async def test_increment_quantity(client):
    """
    Increments the quantity of the existing card in the collection
    and verifies that the new total reflects the change.
    """
    if not card_added:
        pytest.skip("Card was not added successfully in the previous test.")

    response = await client.post(
        "/collection/add",
        params={"card_number": TEST_CARD_NUMBER, "quantity": 2},
        headers=HEADERS,
    )

    assert response.status_code == 200

    response_check = await client.get("/collection/", headers=HEADERS)
    cards = response_check.json()
    card = next((c for c in cards if c["card_number"] == TEST_CARD_NUMBER), None)

    assert card is not None
    assert card["quantity"] == 3


@pytest.mark.order(5)
@pytest.mark.asyncio
async def test_pagination(client):
    """
    Validates that pagination parameters are respected by the /collection/ endpoint.
    Confirms that result sets are limited based on page and per_page values.
    """
    resp1 = await client.get("/collection/?page=1&per_page=1", headers=HEADERS)
    assert resp1.status_code == 200
    assert isinstance(resp1.json(), list)
    assert len(resp1.json()) <= 1

    resp2 = await client.get("/collection/?page=2&per_page=1", headers=HEADERS)
    assert resp2.status_code == 200
    assert isinstance(resp2.json(), list)
    assert len(resp2.json()) <= 1


@pytest.mark.order(6)
@pytest.mark.asyncio
async def test_delete_card(client):
    """
    Deletes the previously added card from the collection.
    Confirms that the card no longer appears in subsequent queries.
    """
    response = await client.delete(
        f"/collection/delete/{TEST_CARD_NUMBER}", headers=HEADERS
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Card removed from collection"

    response_check = await client.get("/collection/", headers=HEADERS)
    cards = response_check.json()
    card = next((c for c in cards if c["card_number"] == TEST_CARD_NUMBER), None)

    assert card is None


@pytest.mark.order(7)
@pytest.mark.asyncio
async def test_delete_card_again_should_fail(client):
    """
    Attempts to delete the same card again.
    Verifies that a 404 error is returned since the card no longer exists.
    """
    response = await client.delete(
        f"/collection/delete/{TEST_CARD_NUMBER}", headers=HEADERS
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Card not found in collection"


@pytest.mark.order(8)
@pytest.mark.asyncio
async def test_invalid_parameters(client):
    """
    Validates error handling for invalid query and input parameters.
    Covers page numbers, per_page limits, and invalid card quantities.
    """

    # Invalid page number (must be >= 1)
    resp1 = await client.get("/collection/?page=0", headers=HEADERS)
    assert resp1.status_code == 422

    # per_page value exceeding allowed range
    resp2 = await client.get("/collection/?per_page=999", headers=HEADERS)
    assert resp2.status_code == 422

    # Negative quantity not allowed when adding a card
    resp3 = await client.post(
        "/collection/add",
        params={"card_number": TEST_CARD_NUMBER, "quantity": -1},
        headers=HEADERS,
    )
    assert resp3.status_code == 422
