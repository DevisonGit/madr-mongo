import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.madr.database import get_session


@pytest.mark.asyncio
async def test_get_session():
    session_generator = get_session()
    session: AsyncSession = await anext(session_generator)
    assert isinstance(session, AsyncSession)
    await session_generator.aclose()
