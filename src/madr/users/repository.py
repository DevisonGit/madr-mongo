from bson import ObjectId

from src.madr.database import db

users_collection = db['users']


def user_helper(user) -> dict:
    return {
        'id': str(user['_id']),
        'name': user['username'],
        'email': user['email'],
    }


async def get_user_by_email(email: str):
    return await users_collection.find_one({'email': email})


async def create_user(user_data: dict):
    result = await users_collection.insert_one(user_data)
    new_user = await users_collection.find_one({'_id': result.inserted_id})
    return user_helper(new_user)


async def update_user(user_id: str, user_data: dict):
    await users_collection.update_one(
        {'_id': ObjectId(user_id)}, {'$set': user_data}
    )
    updated_user = await users_collection.find_one({'_id': ObjectId(user_id)})
    return user_helper(updated_user)


async def delete_user(user_id: str):
    return await users_collection.delete_one({'_id': ObjectId(user_id)})
