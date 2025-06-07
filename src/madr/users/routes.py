from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.madr.database import get_session
from src.madr.shared.schema import Message
from src.madr.users.schemas import UserCreate, UserPublic, UserUpdate
from src.madr.users.service import (
    create_user_service,
    delete_user_service,
    update_user_service,
)

router = APIRouter(prefix='/users', tags=['users'])
Session = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserCreate, session: Session):
    return create_user_service(user, session)


@router.put('/{_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
async def update_user(_id: int, user: UserUpdate, session: Session):
    return update_user_service(_id, user, session)


@router.delete('/{_id}', status_code=HTTPStatus.OK, response_model=Message)
async def delete_user(_id: int, session: Session):
    delete_user_service(_id, session)
    return {'message': 'User deleted'}
