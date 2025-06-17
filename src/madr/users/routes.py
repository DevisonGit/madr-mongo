from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorCollection

from src.madr.database import get_users_collection
from src.madr.security import get_current_user
from src.madr.users import service
from src.madr.users.schemas import UserCreate, UserPublic, UserUpdate

router = APIRouter(prefix='/users', tags=['users'])
CurrentUser = Annotated[UserPublic, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED)
async def create_user(
    user: UserCreate,
    users_collection: AsyncIOMotorCollection = get_users_collection(),
):
    return await service.create_user(user, users_collection)


@router.put('/{user_id}')
async def update_user(
    user_id: str,
    user: UserUpdate,
    current_user: CurrentUser,
    users_collection: AsyncIOMotorCollection = get_users_collection(),
):
    return await service.update_user(
        user_id, user, current_user, users_collection
    )


@router.delete('/{user_id}')
async def delete_user(
    user_id: str,
    current_user: CurrentUser,
    users_collection: AsyncIOMotorCollection = get_users_collection(),
):
    return await service.delete_user(user_id, current_user, users_collection)
