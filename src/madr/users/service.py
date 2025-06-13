from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.madr.security import get_password_hash
from src.madr.users.models import User
from src.madr.users.repository import (
    create_user,
    delete_user,
    get_user,
    update_user,
)
from src.madr.users.schemas import UserCreate, UserUpdate
from src.madr.utils.sanitize import name_in


async def create_user_service(user: UserCreate, session: AsyncSession):
    existing_user = await get_user(user.username, user.email, session)
    if existing_user:
        if existing_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif existing_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Email already exists'
            )

    user_db = User(**user.model_dump())
    user_db.username = name_in(user_db.username)
    user_db.password = get_password_hash(user_db.password)

    return await create_user(user_db, session)


async def update_user_service(
    user_id: int, user: UserUpdate, session: AsyncSession, current_user: User
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    user_db = user.model_dump()
    user_db['username'] = name_in(user_db['username'])
    user_db['password'] = get_password_hash(user_db['password'])
    for key, value in user_db.items():
        setattr(current_user, key, value)

    return await update_user(current_user, session)


async def delete_user_service(
    user_id: int, session: AsyncSession, current_user: User
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    await delete_user(current_user, session)
    return {'message': 'User deleted'}
