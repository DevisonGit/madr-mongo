from bson import ObjectId
from pydantic import EmailStr


def user_helper(user) -> dict:
    return {
        'id': str(user['_id']),
        'username': user['username'],
        'email': user['email'],
    }


async def get_user_by_email(email: EmailStr, users_collection):
    return await users_collection.find_one({'email': email})


async def get_user_by_username(username: str, users_collection):
    return await users_collection.find_one({'username': username})


async def create_user(user_data: dict, users_collection):
    result = await users_collection.insert_one(user_data)
    new_user = await users_collection.find_one({'_id': result.inserted_id})
    return user_helper(new_user)


async def update_user(user_id: str, user_data: dict, users_collection):
    await users_collection.update_one(
        {'_id': ObjectId(user_id)}, {'$set': user_data}
    )
    updated_user = await users_collection.find_one({'_id': ObjectId(user_id)})
    return user_helper(updated_user)


async def delete_user(user_id: str, users_collection):
    return await users_collection.delete_one({'_id': ObjectId(user_id)})
