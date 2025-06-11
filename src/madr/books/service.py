from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.madr.authors.repository import get_author_by_id
from src.madr.books.models import Book
from src.madr.books.repository import (
    create_book,
    delete_book,
    get_book_id,
    get_books,
    patch_book,
)
from src.madr.books.schemas import BookCreate, BookFilter, BookUpdate
from src.madr.utils.sanitize import name_in, name_in_out


async def create_book_service(book: BookCreate, session: AsyncSession):
    try:
        author = await get_author_by_id(book.author_id, session)
        if not author:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Author not found'
            )
        book_db = Book(**book.model_dump())
        book_db.title = name_in(book_db.title)
        return await create_book(book_db, session)
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=f'{name_in_out(book.title)} already exists in MADR',
        )


async def delete_book_service(book_id: int, session: AsyncSession):
    book = await get_book_id(book_id, session)
    if not book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Book not found in MADR'
        )
    await delete_book(book, session)
    return {'message': 'Book deleted in MADR'}


async def patch_book_service(
    book_id: int, book: BookUpdate, session: AsyncSession
):
    book_db = await get_book_id(book_id, session)
    if not book_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Book not found in MADR'
        )
    if book.author_id:
        author = await get_author_by_id(book.author_id, session)
        if not author:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Author not found'
            )
    if book.title:
        book.title = name_in(book.title)
    return await patch_book(book, book_db, session)


async def get_books_service(book_filter: BookFilter, session: AsyncSession):
    books = await get_books(book_filter, session)
    return {'books': books}


async def get_book_service(book_id: int, session: AsyncSession):
    book_db = await get_book_id(book_id, session)
    if not book_db:
        if not book_db:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Book not found in MADR',
            )
    return book_db
