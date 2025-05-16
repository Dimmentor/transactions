from datetime import timedelta
from sqlalchemy import select
from app.models.transaction import Transaction
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger("bboom")
logger.setLevel(logging.INFO)


async def check_spending_limits(
    session: AsyncSession,
    user_id: int,
    tx_date,
    new_amount: float,
    daily_limit: float = 5000.0,
    weekly_limit: float = 30000.0
):
    if new_amount >= 0:
        return

    #Получаем все оплаты за 6 дней
    start_date = tx_date - timedelta(days=6)
    end_date = tx_date + timedelta(days=1)

    stmt = select(Transaction).where(
        Transaction.user_id == user_id,
        Transaction.amount < 0,
        Transaction.timestamp >= start_date,
        Transaction.timestamp < end_date
    )

    result = await session.execute(stmt)
    transactions = result.scalars().all()

    spent_today = abs(new_amount) + sum(
        abs(tx.amount) for tx in transactions if tx.timestamp.date() == tx_date
    )

    new_week = tx_date.isocalendar()[1]
    new_year = tx_date.isocalendar()[0]

    spent_week = abs(new_amount) + sum(
        abs(tx.amount)
        for tx in transactions
        if tx.timestamp.date().isocalendar()[0] == new_year and
           tx.timestamp.date().isocalendar()[1] == new_week
    )

    if spent_today > daily_limit:
        logger.warning(f"Ежедневный лимит в {daily_limit} превышен")

    if spent_week > weekly_limit:
        logger.warning(f"Еженедельный лимит в {weekly_limit} превышен")