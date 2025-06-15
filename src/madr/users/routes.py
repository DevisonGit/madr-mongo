from typing import Annotated

from fastapi import APIRouter, Depends

from src.madr.security import get_current_user
from src.madr.users import service
from src.madr.users.schemas import UserCreate, UserPublic, UserUpdate

router = APIRouter(prefix='/users', tags=['users'])
CurrentUser = Annotated[UserPublic, Depends(get_current_user)]


@router.post('/')
async def create_user(user: UserCreate):
    return await service.create_user(user)


@router.put('/{user_id}')
async def update_user(
    user_id: str, user: UserUpdate, current_user: CurrentUser
):
    return await service.update_user(user_id, user, current_user)


@router.delete('/{user_id}')
async def delete_user(user_id: str, current_user: CurrentUser):
    return await service.delete_user(user_id, current_user)
