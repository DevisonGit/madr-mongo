from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.madr.users.repository import (
    create_user,
    delete_user,
    get_user,
    get_user_id,
    update_user,
)
from src.madr.users.schemas import UserCreate, UserUpdate


def create_user_service(user: UserCreate, session: Session):
    existing_user = get_user(user.username, user.email, session)
    if existing_user:
        if existing_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif existing_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Email already exists'
            )
    return create_user(user, session)


def update_user_service(_id: int, user: UserUpdate, session: Session):
    db_user = get_user_id(_id, session)
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    return update_user(user, db_user, session)


def delete_user_service(_id: int, session: Session):
    db_user = get_user_id(_id, session)
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    return delete_user(db_user, session)
