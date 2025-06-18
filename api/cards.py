from fastapi import APIRouter, Query, Depends, HTTPException
from core.security import api_key_auth
from db.sql import (
    get_all_cards,
    get_all_cards_full_info,
    get_single_card_by_card_number,
    get_card_with_alternatives_by_card_number,
    search_cards_by_name,
    search_cards_with_alternatives_by_name,
)

router = APIRouter(
    prefix="/cards",
    tags=["Cards"],
    dependencies=[Depends(api_key_auth)],
)

@router.get("/", summary="Get paginated list of cards")
def list_cards(
    page: int = Query(1, gt=0, description="Page number for pagination"),
    per_page: int = Query(10, gt=0, le=100, description="Number of items per page"),
    include_alternative: bool = Query(True, description="Include alternative artwork versions"),
):
    """
    Retrieves a paginated list of all cards with basic information.
    """
    return get_all_cards(page, per_page, include_alternative)

@router.get("/full/", summary="Get cards with full details")
def list_cards_full_info(
    page: int = Query(1, gt=0, description="Page number for pagination"),
    per_page: int = Query(10, gt=0, le=100, description="Number of items per page"),
    include_alternative: bool = Query(True, description="Include alternative artwork versions"),
):
    """
    Retrieves a paginated list of all cards with complete details.
    """
    return get_all_cards_full_info(page, per_page, include_alternative)

@router.get("/{card_number}", summary="Get card by card number")
def get_card(card_number: str):
    """
    Retrieves a single main card by its unique card number.
    """
    card = get_single_card_by_card_number(card_number)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card

@router.get("/{card_number}/alternatives", summary="Get card with alternative versions")
def get_card_alternatives(card_number: str):
    """
    Retrieves a card and all its alternative artwork versions.
    """
    cards = get_card_with_alternatives_by_card_number(card_number)
    if not cards:
        raise HTTPException(status_code=404, detail="Card not found")
    return cards

@router.get("/search/", summary="Search cards by name")
def search_cards(
    name_part: str = Query(..., min_length=2, description="Partial card name to search"),
):
    """
    Searches for cards by name without including alternative versions.
    """
    return search_cards_by_name(name_part)

@router.get("/search-with-alternatives/", summary="Search cards with alternatives")
def search_cards_with_alternatives(
    name_part: str = Query(..., min_length=2, description="Partial card name to search"),
):
    """
    Searches for cards by name including their alternative artwork versions.
    """
    return search_cards_with_alternatives_by_name(name_part)
