from fastapi import APIRouter, Query, Depends, HTTPException, Response
from core.security import api_key_auth
from db.sql import (
    get_all_cards,
    get_all_cards_full_info,
    get_single_card_by_card_number,
    get_card_with_alternatives_by_card_number,
    search_cards_by_name,
    search_cards_with_alternatives_by_name,
    get_all_cards_with_ids
)

router = APIRouter(
    prefix="/cards",
    tags=["Cards"],
    dependencies=[Depends(api_key_auth)],
)


@router.get("/", summary="Get all cards")
def list_cards(
    include_alternative: bool = Query(True, description="Include alternative artwork versions"),
):
    cards = get_all_cards(include_alternative)
    if cards is None:
        raise HTTPException(
            status_code=500, detail="Internal server error retrieving cards"
        )
    return cards


@router.get("/ids/", summary="Get all cards with foreign key IDs instead of names")
def list_cards_with_ids(
    include_alternative: bool = Query(True, description="Include alternative artwork versions"),
):
    cards = get_all_cards_with_ids(include_alternative)
    if cards is None:
        raise HTTPException(
            status_code=500, detail="Internal server error retrieving cards"
        )
    return cards


@router.get("/full/", summary="Get cards with full details")
def list_cards_full_info(
    include_alternative: bool = Query(True, description="Include alternative artwork versions"),
):
    cards = get_all_cards_full_info(include_alternative)
    if cards is None:
        raise HTTPException(
            status_code=500, detail="Internal server error retrieving cards"
        )
    return cards


@router.get("/{card_number}", summary="Get card by card number")
def get_card(card_number: str):
    try:
        card = get_single_card_by_card_number(card_number)
    except Exception:
        # This indicates that there was a problem with the query or server
        raise HTTPException(
            status_code=500, detail="Internal server error retrieving card"
        )
    if not card:
        # This indicates that the chart is not in the database.
        raise HTTPException(status_code=404, detail="Card not found")
    return card


@router.get("/{card_number}/alternatives", summary="Get card with alternative versions")
def get_card_alternatives(card_number: str):
    try:
        cards = get_card_with_alternatives_by_card_number(card_number)
    except Exception:
        # This indicates that there was a problem with the query or server
        raise HTTPException(
            status_code=500, detail="Internal server error retrieving cards"
        )
    if not cards:
        # This indicates that the chart is not in the database.
        raise HTTPException(status_code=404, detail="Card not found")
    return cards


@router.get("/search/", summary="Search cards by name")
def search_cards(
    name_part: str = Query(..., min_length=2, description="Partial card name to search")
):
    try:
        cards = search_cards_by_name(name_part)
    except Exception:
        # This indicates that there was a problem with the query or server
        raise HTTPException(
            status_code=500, detail="Internal server error during search"
        )
    if not cards:
        # This indicates that the chart is not in the database.
        raise HTTPException(
            status_code=204, detail="No cards matching the search found"
        )
    return cards


@router.get("/search-with-alternatives/", summary="Search cards with alternatives")
def search_cards_with_alternatives(
    name_part: str = Query(..., min_length=2, description="Partial card name to search")
):
    try:
        cards = search_cards_with_alternatives_by_name(name_part)
    except Exception:
        # This indicates that there was a problem with the query or server
        raise HTTPException(
            status_code=500, detail="Internal server error during search"
        )
    if not cards:
        # This indicates that the chart is not in the database.
        raise HTTPException(
            status_code=204, detail="No cards matching the search found"
        )
    return cards
