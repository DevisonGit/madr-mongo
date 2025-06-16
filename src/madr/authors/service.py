from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException

from src.madr.authors.repository import (
    create_author,
    delete_author,
    get_author_by_id,
    get_authors,
    patch_author,
)
from src.madr.authors.schemas import AuthorCreate, AuthorUpdate, FilterAuthor
from src.madr.utils.sanitize import name_in


async def create_author_service(author: AuthorCreate, authors_collection):
    author_dict = author.model_dump()
    author_dict['name'] = name_in(author_dict['name'])
    author_dict['created_at'] = datetime.now()
    author_dict['updated_at'] = datetime.now()
    return await create_author(author_dict, authors_collection)


async def delete_author_service(author_id: str, authors_collection):
    author = await get_author_by_id(author_id, authors_collection)
    if not author:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Author not found in MADR'
        )
    await delete_author(author_id, authors_collection)
    return {'message': 'Author deleted in MADR'}


async def patch_author_service(
    author_id: str, author: AuthorUpdate, authors_collection
):
    author_db = await get_author_by_id(author_id, authors_collection)
    if not author_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Author not found in MADR'
        )
    author_dict = author.model_dump(exclude_unset=True)
    author_dict['name'] = name_in(author_dict['name'])
    author_dict['updated_at'] = datetime.now()
    author_dict = {k: v for k, v in author_dict.items()}
    return await patch_author(author_id, author_dict, authors_collection)


async def get_author_service(author_id: str, authors_collection):
    author = await get_author_by_id(author_id, authors_collection)
    if not author:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Author not found in MADR'
        )
    return author


async def get_authors_service(author_filter: FilterAuthor, authors_collection):
    author = await get_authors(author_filter, authors_collection)
    return {'authors': author}
