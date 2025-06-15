from bson import ObjectId

from src.madr.authors.schemas import AuthorPublic, FilterAuthor
from src.madr.database import db

authors_collection = db['authors']


def author_helper(author):
    author['id'] = str(author['_id'])
    return author


async def get_author_by_id(author_id: str):
    author = await authors_collection.find_one({'_id': ObjectId(author_id)})
    author = author_helper(author)
    return AuthorPublic(**author)


async def create_author(author_data: dict):
    result = await authors_collection.insert_one(author_data)
    new_author = await authors_collection.find_one({'_id': result.inserted_id})
    new_author = author_helper(new_author)
    return AuthorPublic(**new_author)


async def delete_author(author_id: str):
    return await authors_collection.delete_one({'_id': ObjectId(author_id)})


async def patch_author(author_id: str, author_data: dict):
    await authors_collection.update_one(
        {'_id': ObjectId(author_id)}, {'$set': author_data}
    )
    updated_author = await authors_collection.find_one({
        '_id': ObjectId(author_id)
    })
    updated_author = author_helper(updated_author)
    return AuthorPublic(**updated_author)


async def get_authors(author_filter: FilterAuthor):
    query = {}
    if author_filter.name:
        query['name'] = {'$regex': author_filter.name, '$options': 'i'}
    cursor = (
        authors_collection.find(query)
        .skip(author_filter.offset)
        .limit(author_filter.limit)
    )
    authors = await cursor.to_list(length=author_filter.limit)
    authors = [AuthorPublic(**author_helper(author)) for author in authors]
    return authors
