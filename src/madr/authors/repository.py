from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.madr.authors.models import Author
from src.madr.authors.schemas import AuthorUpdate, FilterAuthor


async def get_author_by_id(author_id: int, session: AsyncSession):
    return await session.scalar(select(Author).where(Author.id == author_id))


async def create_author(author_data: Author, session: AsyncSession):
    session.add(author_data)
    await session.commit()
    await session.refresh(author_data)
    return author_data


async def delete_author(author_data: Author, session: AsyncSession):
    await session.delete(author_data)
    await session.commit()
    return True


async def patch_author(
    author_data: AuthorUpdate, author_db: Author, session: AsyncSession
):
    data = author_data.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(author_db, key, value)
    await session.commit()
    await session.refresh(author_db)
    return author_db


async def get_authors(author_filter: FilterAuthor, session: AsyncSession):
    query = select(Author)
    if author_filter.name:
        query = query.filter(Author.name.contains(author_filter.name))
    authors = await session.scalars(
        query.offset(author_filter.offset).limit(author_filter.limit)
    )
    authors = authors.all()
    return authors
