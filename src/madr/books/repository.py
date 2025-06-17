from bson import ObjectId

from src.madr.books.schemas import BookFilter


async def create_book(book_dict: dict, book_collection):
    result = await book_collection.insert_one(book_dict)
    return await book_collection.find_one({'_id': result.inserted_id})


async def delete_book(book_id: str, book_collection):
    return await book_collection.delete_one({'_id': ObjectId(book_id)})


async def get_book_id(book_id: str, book_collection):
    return await book_collection.find_one({'_id': ObjectId(book_id)})


async def patch_book(book_id: str, book: dict, book_collection):
    await book_collection.update_one(
        {'_id': ObjectId(book_id)}, {'$set': book}
    )
    return await book_collection.find_one({'_id': ObjectId(book_id)})


async def get_books(book_filter: BookFilter, book_collection):
    query = {}
    if book_filter.title:
        query['title'] = {'$regex': book_filter.title, '$options': 'i'}
    if book_filter.year:
        query['year'] = book_filter.year
    cursor = (
        book_collection.find(query)
        .skip(book_filter.offset)
        .limit(book_filter.limit)
    )
    return await cursor.to_list(length=book_filter.limit)
