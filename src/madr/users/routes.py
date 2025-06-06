from http import HTTPStatus

from fastapi import APIRouter

from src.madr.shared.schema import Message
from src.madr.users.schemas import UserCreate, UserPublic, UserUpdate

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserCreate):
    user = UserPublic(**user.model_dump())
    user.id = 1
    return user


@router.put('/{id}', status_code=HTTPStatus.OK, response_model=UserPublic)
async def update_user(id: int, user: UserUpdate):
    user = UserPublic(**user.model_dump())
    user.id = id
    return user


@router.delete('/{id}', status_code=HTTPStatus.OK, response_model=Message)
async def delete_user(id: int):
    return {'message': 'Conta deletada com sucesso'}
