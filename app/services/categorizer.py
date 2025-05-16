from functools import lru_cache

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category

CATEGORY_KEYWORDS = {
    "Food": ["restaurant", "cafe", "snackbar", "pizzeria"],
    "Transport": ["taxi", "bus", "metro", "airplane", "car-rent", "ride"],
    "Entertainment": ["cinema", "airsoft", "paintball"],
    "Utilities": ["electricity", "water", "gas"],
}


async def categorize_transaction(description: str) -> str:
    desc = description.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(word in desc for word in keywords):
            return category
    return "Other"


@lru_cache(maxsize=1000)
async def get_category_by_name(session: AsyncSession, name: str) -> Category:
    result = await session.execute(select(Category).where(Category.name == name))
    return result.scalar_one_or_none()


async def get_or_create_category(session: AsyncSession, name: str) -> Category:
    category = await get_category_by_name(session, name)
    if not category:
        category = Category(name=name)
        session.add(category)
        await session.flush()
    return category
