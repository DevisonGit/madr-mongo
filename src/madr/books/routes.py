from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query

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
from src.madr.security import get_current_user
from src.madr.shared.schema import Message
from src.madr.users.schemas import UserPublic

router = APIRouter(prefix='/books', tags=['books'])
CurrentUser = Annotated[UserPublic, Depends(get_current_user)]
Filter = Annotated[BookFilter, Query()]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=BookPublic)
async def create_book(book: BookCreate, current_user: CurrentUser):
    return await create_book_service(book)


@router.delete('/{book_id}', response_model=Message)
async def delete_book(book_id: str, current_user: CurrentUser):
    return await delete_book_service(book_id)


@router.patch('/{book_id}', response_model=BookPublic)
async def patch_book(
    book_id: str, book: BookUpdate, current_user: CurrentUser
):
    return await patch_book_service(book_id, book)


@router.get('/', response_model=BookList)
async def get_books(book_filter: Filter):
    return await get_books_service(book_filter)


@router.get('/{book_id}', response_model=BookPublic)
async def get_book(book_id: str):
    return await get_book_service(book_id)
