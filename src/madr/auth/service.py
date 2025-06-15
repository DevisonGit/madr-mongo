from http import HTTPStatus

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.madr.auth.repository import get_user_id
from src.madr.database import db
from src.madr.security import (
    create_access_token,
    verify_password,
)
from src.madr.users.models import User


from fastapi import HTTPException
from http import HTTPStatus

users_collection = db['users']

async def get_user_by_username(username: str):
    user_data = await users_collection.find_one({"username": username})
    if user_data:
        user_data["_id"] = str(user_data["_id"])  # 👈 conversão aqui
        return User(**user_data)
    return None

async def create_token_service(form_data: OAuth2PasswordRequestForm):
    user = await get_user_by_username(form_data.username)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}



def refresh_token_service(current_user: User):
    access_token = create_access_token(data={'sub': current_user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}
