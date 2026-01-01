from fastapi import APIRouter, Depends, HTTPException
from core.security import api_key_auth
from db.sql import (
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
)

router = APIRouter(
    prefix="/aux",
    tags=["Auxiliary Tables"],
    dependencies=[Depends(api_key_auth)],
)


@router.get("/bts", summary="Get all BT sets")
def get_all_bts_endpoint():
    """Retrieves all available BT (Booster Set) information"""
    return get_all_bts()


@router.get("/colors", summary="Get all colors")
def get_all_colors_endpoint():
    """Retrieves all available card colors"""
    return get_all_colors()


@router.get("/card-types", summary="Get all card types")
def get_all_card_types_endpoint():
    """Retrieves all available card types (Digimon, Option, Tamer, etc.)"""
    return get_all_card_types()


@router.get("/rarities", summary="Get all rarities")
def get_all_rarities_endpoint():
    """Retrieves all available card rarity levels"""
    return get_all_rarities()


@router.get("/stages", summary="Get all evolution stages")
def get_all_stages_endpoint():
    """Retrieves all available Digimon evolution stages"""
    return get_all_stages()


@router.get("/attributes", summary="Get all attributes")
def get_all_attributes_endpoint():
    """Retrieves all available Digimon attributes"""
    return get_all_attributes()


@router.get("/types", summary="Get all Digimon types")
def get_all_types_endpoint():
    """Retrieves all available Digimon types (Dragon, Beast, etc.)"""
    return get_all_types()


@router.get("/bts/{bt_id}", summary="Get BT set by ID")
def get_bt(bt_id: int):
    """Retrieves a specific BT set by its ID"""
    bt = get_bt_by_id(bt_id)
    if not bt:
        raise HTTPException(status_code=404, detail="BT set not found")
    return bt


@router.get("/colors/{color_id}", summary="Get color by ID")
def get_color(color_id: int):
    """Retrieves a specific color by its ID"""
    color = get_color_by_id(color_id)
    if not color:
        raise HTTPException(status_code=404, detail="Color not found")
    return color


@router.get("/card-types/{card_type_id}", summary="Get card type by ID")
def get_card_type(card_type_id: int):
    """Retrieves a specific card type by its ID"""
    card_type = get_card_type_by_id(card_type_id)
    if not card_type:
        raise HTTPException(status_code=404, detail="Card type not found")
    return card_type


@router.get("/rarities/{rarity_id}", summary="Get rarity by ID")
def get_rarity(rarity_id: int):
    """Retrieves a specific rarity by its ID"""
    rarity = get_rarity_by_id(rarity_id)
    if not rarity:
        raise HTTPException(status_code=404, detail="Rarity not found")
    return rarity


@router.get("/stages/{stage_id}", summary="Get stage by ID")
def get_stage(stage_id: int):
    """Retrieves a specific evolution stage by its ID"""
    stage = get_stage_by_id(stage_id)
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    return stage


@router.get("/attributes/{attribute_id}", summary="Get attribute by ID")
def get_attribute(attribute_id: int):
    """Retrieves a specific attribute by its ID"""
    attribute = get_attribute_by_id(attribute_id)
    if not attribute:
        raise HTTPException(status_code=404, detail="Attribute not found")
    return attribute


@router.get("/types/{type_id}", summary="Get type by ID")
def get_type(type_id: int):
    """Retrieves a specific Digimon type by its ID"""
    digi_type = get_type_by_id(type_id)
    if not digi_type:
        raise HTTPException(status_code=404, detail="Type not found")
    return digi_type
