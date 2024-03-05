from fastapi import APIRouter, Depends, HTTPException, Query, status

from db_api.db import Database
from db_api.dependencies import get_db
from db_api.models.item import Item
from db_api.schemas.item_schema import ItemCreateSchema, ItemSchema

router = APIRouter(tags=["CRUD"])


@router.get("/select", response_model=list[ItemSchema])
async def read(
    is_dirty_read: bool = Query(default=False, alias="is-dirty-read"),
    db: Database = Depends(get_db),
) -> list[Item]:
    items = await db.get_all(is_dirty_read=is_dirty_read)
    return items


@router.post("/insert", status_code=status.HTTP_201_CREATED, response_model=ItemSchema)
async def create(body: ItemCreateSchema, db: Database = Depends(get_db)) -> Item:
    return await db.create(**body.model_dump())


@router.delete("/delete/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(item_id: int, db: Database = Depends(get_db)) -> None:
    item = await db.delete(item_id=item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
