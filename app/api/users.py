from datetime import datetime
from typing import List, Union
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.db.session import get_session
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.stats import StatsResponse
from app.schemas.user import UserCreate, UserRead
from fastapi import Query
from datetime import date
from app.services.analyzer import analyze_transactions

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserRead])
async def list_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    return result.scalars().all()


@router.post("/", response_model=Union[UserRead, List[UserRead]])
async def create_users(
        users: Union[UserCreate, List[UserCreate]],
        session: AsyncSession = Depends(get_session)
):
    if isinstance(users, list):
        to_create = [User(name=u.name) for u in users]
        session.add_all(to_create)
        await session.commit()
        for user in to_create:
            await session.refresh(user)
        return to_create
    else:
        user = User(name=users.name)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


@router.get("/{user_id}/stats", response_model=StatsResponse)
async def get_stats(
        user_id: int,
        from_date: date = Query(..., alias="from"),
        to_date: date = Query(..., alias="to"),
        session: AsyncSession = Depends(get_session),
):

    from_zone = datetime.combine(from_date, datetime.min.time())
    to_zone = datetime.combine(to_date, datetime.max.time())

    stmt = select(Transaction).options(selectinload(Transaction.category)).where(
        Transaction.user_id == user_id,
        Transaction.timestamp >= from_zone,
        Transaction.timestamp <= to_zone
    )
    result = await session.execute(stmt)
    transactions = result.scalars().all()
    return await analyze_transactions(transactions)
