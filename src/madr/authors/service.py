from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.madr.authors.models import Author
from src.madr.authors.repository import (
    create_author,
    delete_author,
    get_author_by_id,
    get_authors,
    patch_author,
)
from src.madr.authors.schemas import AuthorCreate, AuthorUpdate, FilterAuthor
from src.madr.utils.sanitize import name_in, name_in_out


async def create_author_service(author: AuthorCreate, session: AsyncSession):
    try:
        db_author = Author(**author.model_dump())
        db_author.name = name_in(db_author.name)
        return await create_author(db_author, session)
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=f'{name_in_out(author.name)} already exists in MADR',
        )


async def delete_author_service(author_id: int, session: AsyncSession):
    author = await get_author_by_id(author_id, session)
    if not author:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Author not found in MADR'
        )
    await delete_author(author, session)
    return {'message': 'Author deleted in MADR'}


async def patch_author_service(
    author_id: int, author: AuthorUpdate, session: AsyncSession
):
    author_data = await get_author_by_id(author_id, session)
    if not author_data:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Author not found in MADR'
        )
    author.name = name_in(author.name)
    return await patch_author(author, author_data, session)


async def get_author_service(author_id: int, session: AsyncSession):
    author = await get_author_by_id(author_id, session)
    if not author:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Author not found in MADR'
        )
    return author


async def get_authors_service(
    author_filter: FilterAuthor, session: AsyncSession
):
    author = await get_authors(author_filter, session)
    return {'authors': author}
