from http import HTTPStatus

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.madr.auth.repository import get_user_id
from src.madr.security import (
    create_access_token,
    verify_password,
)
from src.madr.users.models import User


async def create_token_service(
    form_data: OAuth2PasswordRequestForm, session: AsyncSession
):
    user = await get_user_id(form_data.username, session)

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
