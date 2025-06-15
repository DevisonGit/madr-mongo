# models/user.py
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from bson import ObjectId


class User(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    username: str
    password: str
    email: EmailStr
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
