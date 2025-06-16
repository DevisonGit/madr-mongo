async def get_user_id(username: str, users_collection):
    result = await users_collection.find_one({'email': username})
    return result
