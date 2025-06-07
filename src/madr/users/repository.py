from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.madr.users.models import User
from src.madr.users.schemas import UserCreate, UserUpdate


def get_user(username: str, email: EmailStr, session: Session):
    return session.scalar(
        select(User).where((User.username == username) | (User.email == email))
    )


def get_user_id(_id: int, session: Session):
    return session.scalar(select(User).where(User.id == _id))


def create_user(user_data: UserCreate, session: Session):
    db_user = User(**user_data.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def update_user(user_data: UserUpdate, user_db: User, session: Session):
    for key, value in user_data.model_dump().items():
        setattr(user_db, key, value)
    session.commit()
    session.refresh(user_db)
    return user_db


def delete_user(db_user: User, session: Session):
    session.delete(db_user)
    session.commit()
    return True
