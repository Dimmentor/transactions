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

    created_transactions = []
    category_cache = {} # Кэш категорий для текущей операции импорта

    for tx_dict in data:
        tx_create = TransactionCreate(**tx_dict)

        existing_tx = await session.get(Transaction, tx_create.id)
        if existing_tx:
            logger.info(f"Пропуск существующих транзакций: {tx_create.id}")
            continue

        # Определение через categorize_transaction в случае отсутствия категории
        cat_name = tx_create.category or await categorize_transaction(tx_create.description or "")

        if cat_name in category_cache:
            category = category_cache[cat_name]
            if not category:
                category = Category(name=cat_name)
                session.add(category)
                await session.flush()
            else:
                pass
        else:
            result = await session.execute(select(Category).where(Category.name == cat_name))
            category = result.scalar_one_or_none()
            if not category:
                category = Category(name=cat_name)
                session.add(category)
                await session.flush()
            category_cache[cat_name] = category

        tx_model = Transaction(
            id=tx_create.id,
            user_id=tx_create.user_id,
            amount=tx_create.amount,
            category_id=category.id,
            timestamp=tx_create.timestamp
        )

        session.add(tx_model)
        created_transactions.append(tx_model)

        await check_spending_limits(
            session=session,
            user_id=tx_create.user_id,
            tx_date=tx_create.timestamp.date(),
            new_amount=tx_create.amount
        )

    await session.commit()

    return created_transactions
