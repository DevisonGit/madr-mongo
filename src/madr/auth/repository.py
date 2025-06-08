from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.madr.users.models import User


def get_user_id(username: str, session: AsyncSession):
    return session.scalar(select(User).where(User.email == username))
