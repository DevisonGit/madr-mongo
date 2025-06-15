from src.madr.database import db

users_collection = db['users']


async def get_user_id(username: str):
    return await users_collection.find_one({'email': username})
