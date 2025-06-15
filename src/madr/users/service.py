from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException

from src.madr.security import get_password_hash
from src.madr.users import repository
from src.madr.users.schemas import UserCreate, UserPublic, UserUpdate
from src.madr.utils.sanitize import name_in


async def create_user(user: UserCreate):
    existing = await repository.get_user_by_email(user.email)
    if existing:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Email already exists'
        )
    user_dict = user.model_dump()
    user_dict['password'] = get_password_hash(user_dict['password'])
    user_dict['username'] = name_in(user_dict['username'])
    user_dict['created_at'] = datetime.now()
    user_dict['updated_at'] = datetime.now()
    return await repository.create_user(user_dict)


async def update_user(
    user_id: str, user: UserUpdate, current_user: UserPublic
):
    if current_user.get('id') != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    user_dict = user.model_dump(exclude_unset=True)
    user_dict['password'] = get_password_hash(user_dict['password'])
    user_dict['username'] = name_in(user_dict['username'])
    user_dict['updated_at'] = datetime.now()
    user_dict = {k: v for k, v in user_dict.items()}
    return await repository.update_user(user_id, user_dict)


async def delete_user(user_id: str, current_user: UserPublic):
    if current_user.get('id') != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    await repository.delete_user(user_id)
    return {'message': 'User deleted'}
