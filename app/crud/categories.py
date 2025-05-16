from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import Category
from app.schemas.category import CategoryCreate


async def create_category(session: AsyncSession, category_create: CategoryCreate) -> Category:
    category = Category(name=category_create.name)
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category
