from http import HTTPStatus

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.madr.auth import repository
from src.madr.security import (
    create_access_token,
    verify_password,
)
from src.madr.users.schemas import UserPublic


async def create_token_service(form_data: OAuth2PasswordRequestForm):
    user = await repository.get_user_id(form_data.username)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    if not verify_password(form_data.password, user.get('password')):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': user.get('email')})

    return {'access_token': access_token, 'token_type': 'bearer'}


def refresh_token_service(current_user: UserPublic):
    access_token = create_access_token(data={'sub': current_user.get('email')})

    return {'access_token': access_token, 'token_type': 'bearer'}
