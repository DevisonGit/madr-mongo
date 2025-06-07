from sqlalchemy import text
from sqlalchemy.orm import Session

from src.madr.database import get_session


def test_get_session():
    session_generator = get_session()
    session = next(session_generator)

    assert isinstance(session, Session)
    session.execute(text("SELECT 1"))

    try:
        next(session_generator)
    except StopIteration:
        pass
