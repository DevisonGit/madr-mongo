from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.madr.database import get_session
from src.madr.security import get_current_user
from src.madr.shared.schema import Message
from src.madr.users.models import User
from src.madr.users.schemas import UserCreate, UserPublic, UserUpdate
from src.madr.users.service import (
    create_user_service,
    delete_user_service,
    update_user_service,
)

router = APIRouter(prefix='/users', tags=['users'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserCreate, session: Session):
    return await create_user_service(user, session)


@router.put('/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
async def update_user(
    user_id: int, user: UserUpdate, session: Session, current_user: CurrentUser
):
    return await update_user_service(user_id, user, session, current_user)


@router.delete('/{user_id}', status_code=HTTPStatus.OK, response_model=Message)
async def delete_user(
    user_id: int, session: Session, current_user: CurrentUser
):
    return await delete_user_service(user_id, session, current_user)
