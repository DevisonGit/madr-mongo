from pydantic import BaseModel

from src.madr.shared.schema import FilterPage


class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    pass


class AuthorPublic(AuthorBase):
    id: int


class FilterAuthor(FilterPage):
    name: str | None = None


class ListAuthor(BaseModel):
    authors: list[AuthorPublic]
