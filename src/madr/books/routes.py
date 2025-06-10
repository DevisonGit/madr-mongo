from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.madr.books.schemas import (
    BookCreate,
    BookFilter,
    BookList,
    BookPublic,
    BookUpdate,
)
from src.madr.books.service import (
    create_book_service,
    delete_book_service,
    get_book_service,
    get_books_service,
    patch_book_service,
)
from src.madr.database import get_session
from src.madr.security import get_current_user
from src.madr.shared.schema import Message
from src.madr.users.models import User

router = APIRouter(prefix='/books', tags=['books'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
Filter = Annotated[BookFilter, Query()]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=BookPublic)
async def create_book(
    book: BookCreate, session: Session, current_user: CurrentUser
):
    return await create_book_service(book, session)


@router.delete('/{book_id}', response_model=Message)
async def delete_book(
    book_id: int, session: Session, current_user: CurrentUser
):
    return await delete_book_service(book_id, session)


@router.patch('/{book_id}', response_model=BookPublic)
async def patch_book(
    book_id: int, book: BookUpdate, session: Session, current_user: CurrentUser
):
    return await patch_book_service(book_id, book, session)


@router.get('/', response_model=BookList)
async def get_books(book_filter: Filter, session: Session):
    return await get_books_service(book_filter, session)


@router.get('/{book_id}', response_model=BookPublic)
async def get_book(book_id: int, session: Session):
    return await get_book_service(book_id, session)
