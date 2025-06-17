import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Query, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from sql import (
    get_all_cards,
    get_all_cards_full_info,
    get_single_card_by_card_number,
    get_card_with_alternatives_by_card_number,
    search_cards_by_name,
    search_cards_with_alternatives_by_name,
    get_all_bts,
    get_all_colors,
    get_all_card_types,
    get_all_rarities,
    get_all_stages,
    get_all_attributes,
    get_all_types,
    get_bt_by_id,
    get_color_by_id,
    get_card_type_by_id,
    get_rarity_by_id,
    get_stage_by_id,
    get_attribute_by_id,
    get_type_by_id,
    get_collection,
    add_card_to_collection,
    delete_card_from_collection,
    get_all_decks,
    create_deck,
    get_deck_cards,
    add_card_to_deck,
    update_card_in_deck,
    delete_card_from_deck,
)


load_dotenv()

# Create FastAPI app with metadata for documentation
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

# Security configuration
API_KEY = os.getenv("API_KEY")

# Create HTTPBearer scheme for Bearer token authentication
security = HTTPBearer()


async def api_key_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Authentication middleware using Bearer token"""
    token = credentials.credentials
    if token != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


# Add security scheme to OpenAPI documentation
from fastapi.openapi.utils import get_openapi


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Add security scheme
    openapi_schema["components"] = {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",  # Optional, but good practice
            }
        }
    }

    # Add security requirement to all operations
    if "paths" in openapi_schema:
        for path in openapi_schema["paths"].values():
            for method in path.values():
                method.setdefault("security", [])
                method["security"].append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# ---------------------------
# API Endpoints
# ---------------------------


@app.get("/cards/", tags=["Cards"], summary="Get paginated list of cards")
def list_cards(
    page: int = Query(1, gt=0, description="Page number for pagination"),
    per_page: int = Query(10, gt=0, le=100, description="Number of items per page"),
    include_alternative: bool = Query(
        True, description="Include alternative artwork versions"
    ),
    token: str = Depends(api_key_auth),
):
    """
    Retrieves a paginated list of all cards with basic information.

    Parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (max: 100)
    - include_alternative: Include alternative artworks (default: True)
    """
    return get_all_cards(page, per_page, include_alternative)


@app.get("/cards/full/", tags=["Cards"], summary="Get cards with full details")
def list_cards_full_info(
    page: int = Query(1, gt=0, description="Page number for pagination"),
    per_page: int = Query(10, gt=0, le=100, description="Number of items per page"),
    include_alternative: bool = Query(
        True, description="Include alternative artwork versions"
    ),
    token: str = Depends(api_key_auth),
):
    """
    Retrieves a paginated list of all cards with complete details.

    Parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (max: 100)
    - include_alternative: Include alternative artworks (default: True)
    """
    return get_all_cards_full_info(page, per_page, include_alternative)


@app.get("/cards/{card_number}", tags=["Cards"], summary="Get card by card number")
def get_card(card_number: str, token: str = Depends(api_key_auth)):
    """
    Retrieves a single main card by its unique card number.

    Parameters:
    - card_number: The unique identifier of the card (e.g., "BT1-001")
    """
    card = get_single_card_by_card_number(card_number)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card


@app.get(
    "/cards/{card_number}/alternatives",
    tags=["Cards"],
    summary="Get card with alternative versions",
)
def get_card_alternatives(card_number: str, token: str = Depends(api_key_auth)):
    """
    Retrieves a card and all its alternative artwork versions.

    Parameters:
    - card_number: The base card number (e.g., "BT1-001")
    """
    cards = get_card_with_alternatives_by_card_number(card_number)
    if not cards:
        raise HTTPException(status_code=404, detail="Card not found")
    return cards


@app.get("/cards/search/", tags=["Cards"], summary="Search cards by name")
def search_cards(
    name_part: str = Query(
        ..., min_length=2, description="Partial card name to search"
    ),
    token: str = Depends(api_key_auth),
):
    """
    Searches for cards by name without including alternative versions.

    Parameters:
    - name_part: Partial card name (minimum 2 characters)
    """
    return search_cards_by_name(name_part)


@app.get(
    "/cards/search-with-alternatives/",
    tags=["Cards"],
    summary="Search cards with alternatives",
)
def search_cards_with_alternatives(
    name_part: str = Query(
        ..., min_length=2, description="Partial card name to search"
    ),
    token: str = Depends(api_key_auth),
):
    """
    Searches for cards by name including their alternative artwork versions.

    Parameters:
    - name_part: Partial card name (minimum 2 characters)
    """
    return search_cards_with_alternatives_by_name(name_part)


# ---------------------------
# Auxiliary Table Endpoints
# ---------------------------


@app.get("/aux/bts", tags=["Auxiliary Tables"], summary="Get all BT sets")
def get_all_bts_endpoint(token: str = Depends(api_key_auth)):
    """Retrieves all available BT (Booster Set) information"""
    return get_all_bts()


@app.get("/aux/colors", tags=["Auxiliary Tables"], summary="Get all colors")
def get_all_colors_endpoint(token: str = Depends(api_key_auth)):
    """Retrieves all available card colors"""
    return get_all_colors()


@app.get("/aux/card-types", tags=["Auxiliary Tables"], summary="Get all card types")
def get_all_card_types_endpoint(token: str = Depends(api_key_auth)):
    """Retrieves all available card types (Digimon, Option, Tamer, etc.)"""
    return get_all_card_types()


@app.get("/aux/rarities", tags=["Auxiliary Tables"], summary="Get all rarities")
def get_all_rarities_endpoint(token: str = Depends(api_key_auth)):
    """Retrieves all available card rarity levels"""
    return get_all_rarities()


@app.get("/aux/stages", tags=["Auxiliary Tables"], summary="Get all evolution stages")
def get_all_stages_endpoint(token: str = Depends(api_key_auth)):
    """Retrieves all available Digimon evolution stages"""
    return get_all_stages()


@app.get("/aux/attributes", tags=["Auxiliary Tables"], summary="Get all attributes")
def get_all_attributes_endpoint(token: str = Depends(api_key_auth)):
    """Retrieves all available Digimon attributes"""
    return get_all_attributes()


@app.get("/aux/types", tags=["Auxiliary Tables"], summary="Get all Digimon types")
def get_all_types_endpoint(token: str = Depends(api_key_auth)):
    """Retrieves all available Digimon types (Dragon, Beast, etc.)"""
    return get_all_types()


@app.get("/aux/bts/{bt_id}", tags=["Auxiliary Tables"], summary="Get BT set by ID")
def get_bt(bt_id: int, token: str = Depends(api_key_auth)):
    """
    Retrieves a specific BT set by its ID

    Parameters:
    - bt_id: Numeric ID of the BT set
    """
    bt = get_bt_by_id(bt_id)
    if not bt:
        raise HTTPException(status_code=404, detail="BT set not found")
    return bt


@app.get("/aux/colors/{color_id}", tags=["Auxiliary Tables"], summary="Get color by ID")
def get_color(color_id: int, token: str = Depends(api_key_auth)):
    """
    Retrieves a specific color by its ID

    Parameters:
    - color_id: Numeric ID of the color
    """
    color = get_color_by_id(color_id)
    if not color:
        raise HTTPException(status_code=404, detail="Color not found")
    return color


@app.get(
    "/aux/card-types/{card_type_id}",
    tags=["Auxiliary Tables"],
    summary="Get card type by ID",
)
def get_card_type(card_type_id: int, token: str = Depends(api_key_auth)):
    """
    Retrieves a specific card type by its ID

    Parameters:
    - card_type_id: Numeric ID of the card type
    """
    card_type = get_card_type_by_id(card_type_id)
    if not card_type:
        raise HTTPException(status_code=404, detail="Card type not found")
    return card_type


@app.get(
    "/aux/rarities/{rarity_id}", tags=["Auxiliary Tables"], summary="Get rarity by ID"
)
def get_rarity(rarity_id: int, token: str = Depends(api_key_auth)):
    """
    Retrieves a specific rarity by its ID

    Parameters:
    - rarity_id: Numeric ID of the rarity
    """
    rarity = get_rarity_by_id(rarity_id)
    if not rarity:
        raise HTTPException(status_code=404, detail="Rarity not found")
    return rarity


@app.get("/aux/stages/{stage_id}", tags=["Auxiliary Tables"], summary="Get stage by ID")
def get_stage(stage_id: int, token: str = Depends(api_key_auth)):
    """
    Retrieves a specific evolution stage by its ID

    Parameters:
    - stage_id: Numeric ID of the evolution stage
    """
    stage = get_stage_by_id(stage_id)
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    return stage


@app.get(
    "/aux/attributes/{attribute_id}",
    tags=["Auxiliary Tables"],
    summary="Get attribute by ID",
)
def get_attribute(attribute_id: int, token: str = Depends(api_key_auth)):
    """
    Retrieves a specific attribute by its ID

    Parameters:
    - attribute_id: Numeric ID of the attribute
    """
    attribute = get_attribute_by_id(attribute_id)
    if not attribute:
        raise HTTPException(status_code=404, detail="Attribute not found")
    return attribute


@app.get("/aux/types/{type_id}", tags=["Auxiliary Tables"], summary="Get type by ID")
def get_type(type_id: int, token: str = Depends(api_key_auth)):
    """
    Retrieves a specific Digimon type by its ID

    Parameters:
    - type_id: Numeric ID of the Digimon type
    """
    digi_type = get_type_by_id(type_id)
    if not digi_type:
        raise HTTPException(status_code=404, detail="Type not found")
    return digi_type


# ---------------------------
# Collection Endpoints
# ---------------------------


@app.get("/collection/", tags=["Collection"], summary="Get user collection")
def get_user_collection(
    page: int = Query(1, gt=0, description="Page number for pagination"),
    per_page: int = Query(25, gt=0, le=100, description="Number of items per page"),
    token: str = Depends(api_key_auth),
):
    """
    Retrieves the user's card collection with pagination

    Parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (max: 100, default: 25)
    """
    return get_collection(page, per_page)


@app.post("/collection/add", tags=["Collection"], summary="Add card to collection")
def add_to_collection(
    card_number: str,
    quantity: int = Query(1, gt=0, description="Quantity to add"),
    token: str = Depends(api_key_auth),
):
    """
    Adds a card to the user's collection or increases its quantity

    Parameters:
    - card_number: The card number to add
    - quantity: Number of copies to add (default: 1)
    """
    success = add_card_to_collection(card_number, quantity)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to add card")
    return {"message": "Card added to collection"}


@app.delete(
    "/collection/delete/{card_number}",
    tags=["Collection"],
    summary="Remove card from collection",
)
def remove_from_collection(card_number: str, token: str = Depends(api_key_auth)):
    """
    Removes a card completely from the user's collection

    Parameters:
    - card_number: The card number to remove
    """
    success = delete_card_from_collection(card_number)
    if not success:
        raise HTTPException(status_code=404, detail="Card not found in collection")
    return {"message": "Card removed from collection"}


# ---------------------------
# Deck Endpoints
# ---------------------------


@app.get("/decks/", tags=["Decks"], summary="Get all decks")
def list_decks(token: str = Depends(api_key_auth)):
    """Retrieves all created decks"""
    return get_all_decks()


@app.post("/decks/add", tags=["Decks"], summary="Create new deck")
def create_new_deck(
    name: str = Query(..., description="Name of the new deck"),
    color_id: Optional[int] = Query(None, description="Primary color ID for the deck"),
    image: Optional[str] = Query(None, description="URL for deck image"),
    token: str = Depends(api_key_auth),
):
    """
    Creates a new empty deck

    Parameters:
    - name: Name for the new deck
    - color_id: Optional color ID for deck theming
    - image: Optional image URL for deck representation
    """
    deck_id = create_deck(name, color_id, image)
    return {"deck_id": deck_id, "message": "Deck created successfully"}


@app.get("/decks/{deck_id}/cards", tags=["Decks"], summary="Get cards in a deck")
def get_deck_cards_endpoint(deck_id: int, token: str = Depends(api_key_auth)):
    """
    Retrieves all cards in a specific deck

    Parameters:
    - deck_id: Numeric ID of the deck
    """
    cards = get_deck_cards(deck_id)
    if not cards:
        raise HTTPException(status_code=404, detail="Deck not found or empty")
    return cards


@app.post("/decks/{deck_id}/cards/add", tags=["Decks"], summary="Add card to deck")
def add_card_to_deck_endpoint(
    deck_id: int,
    card_number: str,
    quantity: int = Query(1, gt=0, description="Quantity to add"),
    token: str = Depends(api_key_auth),
):
    """
    Adds a card to a deck or increases its quantity

    Parameters:
    - deck_id: ID of the target deck
    - card_number: Card number to add
    - quantity: Number of copies to add (default: 1)
    """
    success = add_card_to_deck(deck_id, card_number, quantity)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to add card to deck")
    return {"message": "Card added to deck"}


@app.put(
    "/decks/{deck_id}/cards/update/{card_number}",
    tags=["Decks"],
    summary="Update card quantity in deck",
)
def update_card_quantity_in_deck(
    deck_id: int,
    card_number: str,
    quantity: int = Query(..., ge=0, description="New quantity (0 to remove)"),
    token: str = Depends(api_key_auth),
):
    """
    Updates the quantity of a card in a deck (removes if quantity=0)

    Parameters:
    - deck_id: ID of the target deck
    - card_number: Card number to update
    - quantity: New quantity (0 removes the card)
    """
    success = update_card_in_deck(deck_id, card_number, quantity)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update card quantity")
    return {"message": "Card quantity updated"}


@app.delete(
    "/decks/{deck_id}/cards/delete/{card_number}",
    tags=["Decks"],
    summary="Remove card from deck",
)
def remove_card_from_deck(
    deck_id: int,
    card_number: str,
    token: str = Depends(api_key_auth),
):
    """
    Removes a specific card from a deck completely.

    Parameters:
    - deck_id: ID of the deck
    - card_number: Card number to remove
    """
    success = delete_card_from_deck(deck_id, card_number)
    if not success:
        raise HTTPException(status_code=404, detail="Card not found in deck")
    return {"message": "Card removed from deck"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
