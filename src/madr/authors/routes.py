from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorCollection

from src.madr.authors.schemas import (
    AuthorCreate,
    AuthorPublic,
    AuthorUpdate,
    FilterAuthor,
    ListAuthor,
)
from src.madr.authors.service import (
    create_author_service,
    delete_author_service,
    get_author_service,
    get_authors_service,
    patch_author_service,
)
from src.madr.database import get_authors_collection
from src.madr.security import get_current_user
from src.madr.shared.schema import Message
from src.madr.users.schemas import UserPublic

router = APIRouter(prefix='/authors', tags=['authors'])
CurrentUser = Annotated[UserPublic, Depends(get_current_user)]
Filter = Annotated[FilterAuthor, Query()]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=AuthorPublic)
async def create_author(
    author: AuthorCreate,
    current_user: CurrentUser,
    authors_collection: AsyncIOMotorCollection = get_authors_collection(),
):
    return await create_author_service(author, authors_collection)


@router.delete(
    '/{author_id}', status_code=HTTPStatus.OK, response_model=Message
)
async def delete_author(
    author_id: str,
    current_user: CurrentUser,
    authors_collection: AsyncIOMotorCollection = get_authors_collection(),
):
    return await delete_author_service(author_id, authors_collection)


@router.patch(
    '/{author_id}', status_code=HTTPStatus.OK, response_model=AuthorPublic
)
async def patch_author(
    author_id: str,
    author: AuthorUpdate,
    current_user: CurrentUser,
    authors_collection: AsyncIOMotorCollection = get_authors_collection(),
):
    return await patch_author_service(author_id, author, authors_collection)


@router.get('/{author_id}', response_model=AuthorPublic)
async def get_author(
    author_id: str,
    authors_collection: AsyncIOMotorCollection = get_authors_collection(),
):
    return await get_author_service(author_id, authors_collection)


@router.get('/', response_model=ListAuthor)
async def get_authors(
    author_filter: Filter,
    authors_collection: AsyncIOMotorCollection = get_authors_collection(),
):
    return await get_authors_service(author_filter, authors_collection)
