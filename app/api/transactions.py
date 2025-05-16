from typing import List
from fastapi import APIRouter, Depends, Body, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.session import get_session
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionRead
from app.crud.transactions import create_transaction, delete_transaction, get_transactions
from app.services.importer import import_transactions_from_json

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", response_model=TransactionRead)
async def create(tx: TransactionCreate, session: AsyncSession = Depends(get_session)):
    return await create_transaction(session, tx)


@router.delete("/{tx_id}")
async def delete(tx_id: str, session: AsyncSession = Depends(get_session)):
    await delete_transaction(session, tx_id)
    return {"status": "deleted"}


@router.post("/import")
async def import_from_json(
        file_path: str = Body(..., embed=True),
        session: AsyncSession = Depends(get_session)
):
    txs = await import_transactions_from_json(session, file_path)
    return {"imported": len(txs)}


@router.get("/", response_model=List[TransactionRead])
async def list_transactions(
        user_id: int = Query(None),
        session: AsyncSession = Depends(get_session)
):
    stmt = select(Transaction).options(selectinload(Transaction.category))
    if user_id:
        stmt = stmt.where(Transaction.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().all()
