from fastapi import APIRouter, Query, Depends, HTTPException
from core.security import api_key_auth
from db.sql import get_collection, add_card_to_collection, delete_card_from_collection

router = APIRouter(
    prefix="/collection",
    tags=["Collection"],
    dependencies=[Depends(api_key_auth)],
)


@router.get("/", summary="Get user collection")
def get_user_collection(
    page: int = Query(1, gt=0, description="Page number for pagination"),
    per_page: int = Query(25, gt=0, le=100, description="Number of items per page"),
):
    """
    Retrieves the user's card collection with pagination.

    Parameters:
    - page: Page number (default: 1)
    - per_page: Items per page (max: 100, default: 25)
    """
    return get_collection(page, per_page)


@router.post("/add", summary="Add card to collection")
def add_to_collection(
    card_number: str,
    quantity: int = Query(1, gt=0, description="Quantity to add"),
):
    """
    Adds a card to the user's collection or increases its quantity.

    Parameters:
    - card_number: The card number to add
    - quantity: Number of copies to add (default: 1)
    """
    success = add_card_to_collection(card_number, quantity)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to add card")
    return {"message": "Card added to collection"}


@router.delete("/delete/{card_number}", summary="Remove card from collection")
def remove_from_collection(card_number: str):
    """
    Removes a card completely from the user's collection.

    Parameters:
    - card_number: The card number to remove
    """
    success = delete_card_from_collection(card_number)
    if not success:
        raise HTTPException(status_code=404, detail="Card not found in collection")
    return {"message": "Card removed from collection"}
