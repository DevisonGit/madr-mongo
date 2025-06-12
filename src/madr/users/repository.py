from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.madr.users.models import User


async def get_user(username: str, email: EmailStr, session: AsyncSession):
    return await session.scalar(
        select(User).where((User.username == username) | (User.email == email))
    )


async def create_user(user_data: User, session: AsyncSession):
    session.add(user_data)
    await session.commit()
    await session.refresh(user_data)
    return user_data


async def update_user(user_db: User, session: AsyncSession):
    await session.commit()
    await session.refresh(user_db)
    return user_db


async def delete_user(db_user: User, session: AsyncSession):
    await session.delete(db_user)
    await session.commit()
    return True
