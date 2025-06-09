from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

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
from src.madr.database import get_session
from src.madr.security import get_current_user
from src.madr.shared.schema import Message
from src.madr.users.models import User

router = APIRouter(prefix='/authors', tags=['authors'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
Filter = Annotated[FilterAuthor, Query()]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=AuthorPublic)
async def create_author(
    author: AuthorCreate, session: Session, current_user: CurrentUser
):
    return await create_author_service(author, session)


@router.delete(
    '/{author_id}', status_code=HTTPStatus.OK, response_model=Message
)
async def delete_author(
    author_id: int, session: Session, current_user: CurrentUser
):
    return await delete_author_service(author_id, session)


@router.patch(
    '/{author_id}', status_code=HTTPStatus.OK, response_model=AuthorPublic
)
async def patch_author(
    author_id: int,
    author: AuthorUpdate,
    session: Session,
    current_user: CurrentUser,
):
    return await patch_author_service(author_id, author, session)


@router.get('/{author_id}', response_model=AuthorPublic)
async def get_author(author_id: int, session: Session):
    return await get_author_service(author_id, session)


@router.get('/', response_model=ListAuthor)
async def get_authors(author_filter: Filter, session: Session):
    return await get_authors_service(author_filter, session)
