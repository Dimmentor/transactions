from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate


async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
    user = User(name=user_create.name)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
