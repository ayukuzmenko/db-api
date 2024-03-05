from fastapi import APIRouter, Depends, HTTPException, status

from db_api.db import Database
from db_api.dependencies import get_db
from db_api.schemas.transaction_schema import TransactionSchema

router = APIRouter(tags=["Transactions"])


@router.post("/begin", response_model=TransactionSchema)
async def begin(db: Database = Depends(get_db)) -> TransactionSchema:
    await db.begin()
    return TransactionSchema(message="transaction started")


@router.post("/commit", response_model=TransactionSchema)
async def commit(db: Database = Depends(get_db)) -> TransactionSchema:
    is_started = await db.check_transaction()
    if not is_started:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="transaction doesn't exist"
        )

    await db.commit()
    return TransactionSchema(message="transaction committed")


@router.post("/rollback", response_model=TransactionSchema)
async def rollback(db: Database = Depends(get_db)) -> TransactionSchema:
    is_started = await db.check_transaction()
    if not is_started:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="transaction doesn't exist"
        )

    await db.rollback()
    return TransactionSchema(message="transaction rolled back")
