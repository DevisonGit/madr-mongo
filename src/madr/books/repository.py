from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.madr.books.models import Book
from src.madr.books.schemas import BookFilter, BookUpdate


async def create_book(book: Book, session: AsyncSession):
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return book


async def delete_book(book: Book, session: AsyncSession):
    await session.delete(book)
    await session.commit()
    return True


async def get_book_id(book_id: int, session: AsyncSession):
    return await session.scalar(select(Book).where(Book.id == book_id))


async def patch_book(book: BookUpdate, book_db: Book, session: AsyncSession):
    data = book.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(book_db, key, value)
    await session.commit()
    await session.refresh(book_db)
    return book_db


async def get_books(book_filter: BookFilter, session: AsyncSession):
    query = select(Book)
    if book_filter.title:
        query = query.filter(Book.title.contains(book_filter.title))
    if book_filter.year:
        query = query.filter(Book.year == book_filter.year)
    books = await session.scalars(
        query.offset(book_filter.offset).limit(book_filter.limit)
    )
    books = books.all()
    return books
