from http import HTTPStatus
from fastapi import HTTPException
from bson import ObjectId

from src.madr.security import get_password_hash
from src.madr.users.models import User
from src.madr.users.schemas import UserCreate, UserUpdate
from src.madr.database import db  # motor client
from src.madr.utils.sanitize import name_in


from datetime import datetime

async def create_user_service(user: UserCreate):
    # Verifica se username ou email já existem
    existing_user = await db.users.find_one({
        "$or": [
            {"username": user.username},
            {"email": user.email}
        ]
    })
    if existing_user:
        if existing_user["username"] == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Username already exists"
            )
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Email already exists"
            )

    now = datetime.now()

    user_dict = user.dict()
    user_dict["username"] = name_in(user_dict["username"])
    user_dict["password"] = get_password_hash(user_dict["password"])
    user_dict["created_at"] = now
    user_dict["updated_at"] = now

    result = await db.users.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)


    return User(**user_dict)



from datetime import datetime

async def update_user_service(user_id: str, user: UserUpdate, current_user: User):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Not enough permissions"
        )
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")

    user_data = user.dict(exclude_unset=True)
    if "username" in user_data:
        user_data["username"] = name_in(user_data["username"])
    if "password" in user_data:
        user_data["password"] = get_password_hash(user_data["password"])

    user_data["updated_at"] = datetime.now()

    result = await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": user_data}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = await db.users.find_one({"_id": ObjectId(user_id)})
    return User(**updated_user)


async def delete_user_service(user_id: str, current_user: User):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Not enough permissions"
        )
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")

    result = await db.users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted"}
