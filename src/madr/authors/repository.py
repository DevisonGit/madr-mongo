from bson import ObjectId

from src.madr.authors.schemas import FilterAuthor


async def get_author_by_id(author_id: str, authors_collection):
    return await authors_collection.find_one({'_id': ObjectId(author_id)})


async def create_author(author_data: dict, authors_collection):
    result = await authors_collection.insert_one(author_data)
    return await authors_collection.find_one({'_id': result.inserted_id})


async def delete_author(author_id: str, authors_collection):
    return await authors_collection.delete_one({'_id': ObjectId(author_id)})


async def patch_author(author_id: str, author_data: dict, authors_collection):
    await authors_collection.update_one(
        {'_id': ObjectId(author_id)}, {'$set': author_data}
    )
    return await authors_collection.find_one({'_id': ObjectId(author_id)})


async def get_authors(author_filter: FilterAuthor, authors_collection):
    query = {}
    if author_filter.name:
        query['name'] = {'$regex': author_filter.name, '$options': 'i'}
    cursor = (
        authors_collection.find(query)
        .skip(author_filter.offset)
        .limit(author_filter.limit)
    )
    return await cursor.to_list(length=author_filter.limit)
