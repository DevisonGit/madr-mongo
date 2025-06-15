# models/book.py
from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    id: Optional[str]
    title: str

# models/author.py
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from src.madr.books.models import Book
from bson import ObjectId

class Author(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    books: List[Book] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
