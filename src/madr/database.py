from http import HTTPStatus

from fastapi import Depends, HTTPException, Request
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from src.madr.settings import Settings


def get_motor_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(Settings().DATABASE_URL)


def get_db_name():
    return Settings().DATABASE_URL.split('/')[-1]


def get_database(client: AsyncIOMotorClient = None):
    if not client:
        client = get_motor_client()
    return client[get_db_name()]


async def get_db_collection(
    request: Request, collection_name: str = 'users'
) -> AsyncIOMotorCollection:
    if not hasattr(request.app, 'mongodb'):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Database client not initialized. Server misconfiguration.',
        )
    return request.app.mongodb[collection_name]


def get_users_collection():
    async def _get_collection(request: Request) -> AsyncIOMotorCollection:
        if not hasattr(request.app, 'mongodb'):
            raise HTTPException(
                status_code=500, detail='MongoDB not initialized.'
            )
        return request.app.mongodb['users']

    return Depends(_get_collection)


def get_authors_collection():
    async def _get_collection(request: Request) -> AsyncIOMotorCollection:
        if not hasattr(request.app, 'mongodb'):
            raise HTTPException(
                status_code=500, detail='MongoDB not initialized.'
            )
        return request.app.mongodb['authors']

    return Depends(_get_collection)


def get_books_collection():
    async def _get_collection(request: Request) -> AsyncIOMotorCollection:
        if not hasattr(request.app, 'mongodb'):
            raise HTTPException(
                status_code=500, detail='MongoDB not initialized.'
            )
        return request.app.mongodb['books']

    return Depends(_get_collection)
