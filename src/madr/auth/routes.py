from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorCollection

from src.madr.auth.schemas import Token
from src.madr.auth.service import create_token_service, refresh_token_service
from src.madr.database import get_users_collection
from src.madr.security import get_current_user
from src.madr.users.schemas import UserPublic

router = APIRouter(prefix='/auth', tags=['auth'])
OAuth2 = Annotated[OAuth2PasswordRequestForm, Depends()]
CurrentUser = Annotated[UserPublic, Depends(get_current_user)]


@router.post('/token')
async def login_for_access_token(
    form_data: OAuth2,
    users_collection: AsyncIOMotorCollection = get_users_collection(),
):
    return await create_token_service(form_data, users_collection)


@router.post('/refresh-token', response_model=Token)
async def refresh_access_token(current_user: CurrentUser):
    return await refresh_token_service(current_user)
