import json
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path
from app.exceptions import FileNotFoundException
from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate
from app.services.categorizer import categorize_transaction
from app.services.limit_checker import check_spending_limits


logger = logging.getLogger("bboom")
logging.basicConfig(level=logging.INFO)


async def import_transactions_from_json(session: AsyncSession, file_path: str):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundException

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    created = []

    for tx_dict in data:
        tx = TransactionCreate(**tx_dict)

        existing = await session.get(Transaction, tx.id)
        if existing:
            logger.info(f"Пропуск существующих транзакций: {tx.id}")
            continue

        category_name = tx.category or await categorize_transaction(tx.description or "")
        result = await session.execute(select(Category).where(Category.name == category_name))
        category = result.scalar_one_or_none()
        if not category:
            category = Category(name=category_name)
            session.add(category)
            await session.flush()
        category_id = category.id

        tx_model = Transaction(
            id=tx.id,
            user_id=tx.user_id,
            amount=tx.amount,
            category_id=category_id,
            timestamp=tx.timestamp
        )
        session.add(tx_model)
        created.append(tx_model)

        await check_spending_limits(
            session=session,
            user_id=tx.user_id,
            tx_date=tx.timestamp.date(),
            new_amount=tx.amount
        )

    await session.commit()
    return created