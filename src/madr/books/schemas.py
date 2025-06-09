from pydantic import BaseModel


class BookBase(BaseModel):
    year: int
    title: str
    author_id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class BookPublic(BookBase):
    id: int
