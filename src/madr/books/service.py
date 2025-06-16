from datetime import datetime
from http import HTTPStatus

from bson import ObjectId
from fastapi import HTTPException

from src.madr.authors.repository import get_author_by_id
from src.madr.books.repository import (
    create_book,
    delete_book,
    get_book_id,
    get_books,
    patch_book,
)
from src.madr.books.schemas import BookCreate, BookFilter, BookUpdate
from src.madr.utils.sanitize import name_in


async def create_book_service(
    book: BookCreate, book_collection, authors_collection
):
    if not ObjectId.is_valid(book.author_id):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='ID invalid'
        )
    author = await get_author_by_id(book.author_id, authors_collection)
    if not author:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Author not found in MADR'
        )
    book_dict = book.model_dump()
    book_dict['title'] = name_in(book_dict['title'])
    book_dict['created_at'] = datetime.now()
    book_dict['updated_at'] = datetime.now()
    return await create_book(book_dict, book_collection)


async def delete_book_service(book_id: str, book_collection):
    if not ObjectId.is_valid(book_id):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='ID invalid'
        )
    book = await get_book_id(book_id, book_collection)
    if not book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Book not found in MADR'
        )
    await delete_book(book_id, book_collection)
    return {'message': 'Book deleted in MADR'}


async def patch_book_service(
    book_id: str, book: BookUpdate, book_collection, authors_collection
):
    book_db = await get_book_id(book_id, book_collection)
    if not book_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Book not found in MADR'
        )
    if book.author_id:
        author = await get_author_by_id(book.author_id, authors_collection)
        if not author:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Author not found'
            )
    if book.title:
        book.title = name_in(book.title)
    book_dict = book.model_dump(exclude_unset=True)
    book_dict['updated_at'] = datetime.now()
    book_dict = {k: v for k, v in book_dict.items()}
    return await patch_book(book_id, book_dict, book_collection)


async def get_books_service(book_filter: BookFilter, book_collection):
    books = await get_books(book_filter, book_collection)
    return {'books': books}


async def get_book_service(book_id: str, book_collection):
    book_db = await get_book_id(book_id, book_collection)
    if not book_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Book not found in MADR',
        )
    return book_db
