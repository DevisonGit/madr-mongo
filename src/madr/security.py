from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from motor.motor_asyncio import AsyncIOMotorCollection
from pwdlib import PasswordHash

from src.madr.database import get_users_collection
from src.madr.settings import Settings

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


async def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('America/Sao_Paulo')) + timedelta(
        minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encode_jwt = encode(
        to_encode, Settings().SECRET_KEY, algorithm=Settings().ALGORITHM
    )
    return encode_jwt


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    users_collection: AsyncIOMotorCollection = get_users_collection(),
):
    credentials_exceptions = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = decode(
            token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM]
        )
        subject_email = payload.get('sub')
        if not subject_email:
            raise credentials_exceptions

    except (DecodeError, ExpiredSignatureError):
        raise credentials_exceptions

    user_data = await users_collection.find_one({'email': subject_email})
    if not user_data:
        raise credentials_exceptions

    user_data['id'] = str(user_data['_id'])
    return user_data
