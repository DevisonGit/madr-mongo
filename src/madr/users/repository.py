from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.madr.security import get_password_hash
from src.madr.users.models import User
from src.madr.users.schemas import UserCreate, UserUpdate


async def get_user(username: str, email: EmailStr, session: AsyncSession):
    return await session.scalar(
        select(User).where((User.username == username) | (User.email == email))
    )


async def create_user(user_data: UserCreate, session: AsyncSession):
    data = user_data.model_dump()
    data['password'] = get_password_hash(data['password'])
    db_user = User(**data)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def update_user(
    user_data: UserUpdate, user_db: User, session: AsyncSession
):
    data = user_data.model_dump()
    data['password'] = get_password_hash(data['password'])
    for key, value in data.items():
        setattr(user_db, key, value)
    await session.commit()
    await session.refresh(user_db)
    return user_db


async def delete_user(db_user: User, session: AsyncSession):
    await session.delete(db_user)
    await session.commit()
    return True
