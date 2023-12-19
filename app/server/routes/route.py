from typing import List

from fastapi import APIRouter, HTTPException

from ..databases.database import items_collection
from ..models.model import Item

router = APIRouter()


@router.get("/items", response_description="List all items", response_model=List[Item])
async def list_all_items():
    items = await items_collection.find().to_list(2)
    return [Item.model_validate_strings(item) for item in items]


@router.post("/item", response_model=Item)
async def create_item(item: Item):
    result = await items_collection.insert_one(item.model_dump())
    item.id = result
    return item


@router.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    item = await items_collection.find_one({"_id": item_id})

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


@router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    updated_item = await items_collection.find_one_and_update(
        {"_id": item_id}, {"$set": item.model_dump_json()}
    )
    if updated_item:
        return item
    raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/items/{item_id}", response_model=Item)
async def delete_item(item_id: str):
    deleted_item = await items_collection.find_one_and_delete({"_id": item_id})
    if deleted_item:
        return deleted_item
    raise HTTPException(status_code=404, detail="Item not found")