from fastapi import APIRouter, Query, Depends, HTTPException
from typing import Optional
from core.security import api_key_auth
from db.sql import (
    get_all_decks,
    create_deck,
    get_deck_cards,
    add_card_to_deck,
    update_card_in_deck,
    delete_card_from_deck,
)

router = APIRouter(
    prefix="/decks",
    tags=["Decks"],
    dependencies=[Depends(api_key_auth)],
)


@router.get("/", summary="Get all decks")
def list_decks():
    """Retrieves all created decks"""
    return get_all_decks()


@router.post("/add", summary="Create new deck")
def create_new_deck(
    name: str = Query(..., description="Name of the new deck"),
    color_id: Optional[int] = Query(None, description="Primary color ID for the deck"),
    image: Optional[str] = Query(None, description="URL for deck image"),
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


@router.get("/{deck_id}/cards", summary="Get cards in a deck")
def get_deck_cards_endpoint(deck_id: int):
    """
    Retrieves all cards in a specific deck

    Parameters:
    - deck_id: Numeric ID of the deck
    """
    cards = get_deck_cards(deck_id)
    if not cards:
        raise HTTPException(status_code=404, detail="Deck not found or empty")
    return cards


@router.post("/{deck_id}/cards/add", summary="Add card to deck")
def add_card_to_deck_endpoint(
    deck_id: int,
    card_number: str,
    quantity: int = Query(1, gt=0, description="Quantity to add"),
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


@router.put(
    "/{deck_id}/cards/update/{card_number}", summary="Update card quantity in deck"
)
def update_card_quantity_in_deck(
    deck_id: int,
    card_number: str,
    quantity: int = Query(..., ge=0, description="New quantity (0 to remove)"),
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


@router.delete("/{deck_id}/cards/delete/{card_number}", summary="Remove card from deck")
def remove_card_from_deck(deck_id: int, card_number: str):
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
