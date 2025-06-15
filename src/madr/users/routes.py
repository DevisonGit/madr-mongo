from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from src.madr.database import db
from src.madr.security import get_current_user
from src.madr.shared.schema import Message
from src.madr.users.models import User  # Pydantic User
from src.madr.users.schemas import UserCreate, UserPublic, UserUpdate
from src.madr.users.service import (
    create_user_service,
    delete_user_service,
    update_user_service,
)
from bson import ObjectId

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserCreate):
    return await create_user_service(user)


@router.put("/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic)
async def update_user(user_id: str, user: UserUpdate, current_user: User = Depends(get_current_user)):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    return await update_user_service(user_id, user, current_user)


@router.delete("/{user_id}", status_code=HTTPStatus.OK, response_model=Message)
async def delete_user(user_id: str, current_user: User = Depends(get_current_user)):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    return await delete_user_service(user_id, current_user)
