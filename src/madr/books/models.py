# models/book.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId


class Book(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    title: str
    year: int
    author_id: str  # Aqui vai o _id do autor (como string)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }

