from fastapi import HTTPException
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select
from app.models.transaction import Transaction
from app.models.user import User
from app.models.category import Category
from app.schemas.transaction import TransactionCreate
from app.services.limit_checker import check_spending_limits
from app.services.categorizer import categorize_transaction


async def create_transaction(session: AsyncSession, tx_data: TransactionCreate) -> Transaction:
    if tx_data.currency != "RUB":
        raise HTTPException(status_code=400, detail="Оплата доступна только рублями")

    user = await session.get(User, tx_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"Пользователя с ID {tx_data.user_id} не существует")

    existing = await session.get(Transaction, tx_data.id)
    if existing:
        raise HTTPException(status_code=400, detail="Транзакция с таким id уже существует")

    category_name = tx_data.category or await categorize_transaction(tx_data.description or "")
    result = await session.execute(select(Category).where(Category.name == category_name))
    category = result.scalar_one_or_none()
    if not category:
        category = Category(name=category_name)
        session.add(category)
        await session.flush()
    category_id = category.id

    tx = Transaction(
        id=tx_data.id,
        user_id=tx_data.user_id,
        amount=tx_data.amount,
        category_id=category_id,
        timestamp=tx_data.timestamp
    )
    session.add(tx)
    await session.commit()
    await session.refresh(tx)

    await check_spending_limits(
        session=session,
        user_id=tx.user_id,
        tx_date=tx.timestamp.date(),
        new_amount=tx.amount
    )

    await session.refresh(tx, attribute_names=["category"])

    return tx


async def get_transactions_by_user_and_period(session: AsyncSession, user_id: int, start: datetime, end: datetime):
    stmt = select(Transaction).where(
        Transaction.user_id == user_id,
        Transaction.timestamp >= start,
        Transaction.timestamp <= end
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_transactions(session: AsyncSession, user_id: int = None):
    stmt = select(Transaction)
    if user_id:
        stmt = stmt.where(Transaction.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def delete_transaction(session: AsyncSession, tx_id: str):
    stmt = delete(Transaction).where(Transaction.id == tx_id)
    await session.execute(stmt)
    await session.commit()
